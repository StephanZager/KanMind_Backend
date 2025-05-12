from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User
from task_app.models import Tasks

class TasksSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Tasks
        fields = '__all__'