from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import TasksSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from task_app.models import Tasks
from user_auth_app.api.permissions import IsOwner


class TasksView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    
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