from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import TasksSerializer, TaskSerializerDetails
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from task_app.models import Tasks
from django.db.models import Q
from user_auth_app.api.permissions import IsOwner


class TasksView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializerDetails

    def get_object(self):
        # Hole die Task basierend auf der pk und den Zugriffsrechten des Benutzers
        try:
            return Tasks.objects.get(
                pk=self.kwargs['pk'],
                board__owner_id=self.request.user
            )
        except Tasks.DoesNotExist:
            return Tasks.objects.get(
                pk=self.kwargs['pk'],
                board__member_count=self.request.user
            )


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
