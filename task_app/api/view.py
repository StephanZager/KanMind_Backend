from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import TasksSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from task_app.models import Tasks


class TasksView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer