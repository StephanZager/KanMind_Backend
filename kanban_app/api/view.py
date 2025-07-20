from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, BoardCreateSerializer, BoardSerializerDetails, TaskSerializer, TaskCreateUpdateSerializer
from django.contrib.auth.models import User
from .permissions import IsOwner, IsMember
from ..models import Board, Tasks
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
