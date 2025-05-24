from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import TasksSerializer, TaskSerializerDetails,CommentSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from task_app.models import Tasks, Comment
from django.db.models import Q
from user_auth_app.api.permissions import IsOwner,IsOwnerOrMember
from .permissions import IsBoardMember, IsCommentAuthor


class TasksView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrMember]
    serializer_class = TaskSerializerDetails

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(
            Q(board__owner_id=user) | Q(board__members=user)
        ).distinct()


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Tasks.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Tasks.objects.filter(reviewer=self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = Tasks.objects.get(id=task_id)
        except Tasks.DoesNotExist:
            raise ValidationError("Task not found.")
        serializer.save(author=self.request.user, task=task)

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        task_id = self.kwargs['task_id']
        comment_id = self.kwargs['comment_id']
        try:
            comment = Comment.objects.get(id=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Comment or Task not found.")
        self.check_object_permissions(self.request, comment)
        return comment