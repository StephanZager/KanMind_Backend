from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User
from task_app.models import Tasks

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']     

class TasksSerializer(serializers.ModelSerializer):
    assignee = MemberSerializer(read_only=True)  
    reviewer = MemberSerializer(read_only=True)
    
    class Meta:

        model = Tasks
        fields = '__all__'
        
   