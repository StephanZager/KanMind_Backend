from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, BoardCreateSerializer, BoardSerializerDetails, TaskSerializer, TaskCreateUpdateSerializer, TaskDetailSerializer, TaskUpdateSerializer, CommentSerializer
from django.contrib.auth.models import User
from .permissions import IsOwner, IsMember, IsBoardMember, CanUpdateOrDestroyTask, CanAccessTaskComments, IsCommentAuthor
from ..models import Board, Tasks, Comment
from django.db.models import Q


class BoardListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = BoardSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BorderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializerDetails

    def get_permissions(self):

        if self.request.method == 'DELETE':
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [
                permissions.IsAuthenticated, IsOwner | IsMember]

        return [permission() for permission in permission_classes]


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(assignee=self.request.user)


class ReviewingTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(reviewer=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):

    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):

        board = serializer.validated_data.get('board')
        if self.request.user not in board.members.all():
            self.permission_denied(
                self.request, message="You must be a member of the board to create a task.")
        serializer.save()


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated, CanUpdateOrDestroyTask]

    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):

        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskDetailSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessTaskComments]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task = get_object_or_404(Tasks, pk=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)
