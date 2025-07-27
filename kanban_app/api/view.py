from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, BoardCreateSerializer, TaskUpdateResponseSerializer, BoardSerializerDetails, TaskSerializer, BoardUpdateResponseSerializer, TaskCreateUpdateSerializer, TaskDetailSerializer, TaskUpdateSerializer, CommentSerializer, BoardUpdateSerializer
from django.contrib.auth.models import User
from .permissions import IsOwner, IsMember, IsBoardMember, CanUpdateOrDestroyTask, CanAccessTaskComments, IsCommentAuthor
from ..models import Board, Tasks, Comment
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

class BoardListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating boards.
    - GET: Returns a list of boards where the user is either the owner or a member.
    - POST: Creates a new board, setting the current user as the owner.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all()

    def get_serializer_class(self):
        """Selects the serializer based on the request method."""
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

    def get_queryset(self):
        """
        Filters the queryset to only include boards relevant to the
        authenticated user (either as owner or member).
        """
        user = self.request.user
        return self.queryset.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """Sets the current user as the owner when creating a new board."""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Custom create method to return the full BoardSerializer representation
        upon successful creation, as per API documentation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = BoardSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BorderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a single board.
    Permissions are dynamically set based on the request method.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializerDetails

    def get_permissions(self):
        """
        Dynamically assigns permissions based on the request method.
        - DELETE: Only the owner can delete.
        - Other methods: Owner or members can access.
        """
        if self.request.method == 'DELETE':
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [
                permissions.IsAuthenticated, (IsOwner | IsMember)
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Selects the serializer for DATA PROCESSING.
        """
        if self.request.method == 'GET':
            return BoardSerializerDetails
        return BoardUpdateSerializer

    def update(self, request, *args, **kwargs):
        """
        Overrides the default update method to the response
        explicitly format it with another serializer.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = BoardUpdateResponseSerializer(
            instance, context=self.get_serializer_context())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(assignee=user)


class ReviewingTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(reviewer=user)


class TaskListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all tasks and creating a new task.
    """
    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Selects the serializer based on the request method."""
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic to verify permissions before creating a task and
        to set the creator automatically.
        """
        board = serializer.validated_data.get('board')
        user = self.request.user

        if user not in board.members.all() and user != board.owner:
            self.permission_denied(
                self.request, message="You must be a member or the owner of the board to create a task."
            )
        serializer.save(creator=user)

    def create(self, request, *args, **kwargs):
        board_id = request.data.get('board')
        if not board_id:
            return Response({'detail': 'Board field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            errors = exc.detail
            # Prüfe, ob der Fehler auf ein nicht gefundenes Board zurückzuführen ist
            if "board" in errors and any("object does not exist" in str(msg) for msg in errors["board"]):
                raise NotFound("Board not found.")
            raise

        self.perform_create(serializer)
        response_serializer = TaskDetailSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a single task.
    Access is controlled by the CanUpdateOrDestroyTask permission class.
    """
    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated, CanUpdateOrDestroyTask]
    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        """
        Selects the appropriate serializer for reading vs. writing.
        - GET: Use TaskDetailSerializer for rich, nested output.
        - PUT/PATCH: Use TaskUpdateSerializer for input validation.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskDetailSerializer

    def update(self, request, *args, **kwargs):
        """
        Overrides the update method after saving the
        to return detailed response using the read serializer.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = TaskUpdateResponseSerializer(instance)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an existing task. Only the task creator or board owner can delete the task.
        Returns an empty response with status 204 if successful.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles listing all comments for a specific task and creating a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessTaskComments]

    def get_queryset(self):
        """Filters comments to only include those for the specified task."""
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        """
        Automatically assigns the current user as the author and associates
        the comment with the correct task from the URL.
        """
        task = get_object_or_404(Tasks, pk=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


class CommentDestroyAPIView(generics.DestroyAPIView):
    """
    Handles the deletion of a single comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        """
        Filters the queryset to ensure the comment belongs to the task
        specified in the URL, preventing accidental deletion across tasks.
        """
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)
