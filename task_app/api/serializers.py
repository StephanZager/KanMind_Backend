from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User
from task_app.models import Tasks

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']     

class TasksSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False)
    reviewer_id = serializers.IntegerField(write_only=True, required=False)
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = '__all__'

    def validate(self, data):
        board = data.get('board')
        assignee_id = data.get('assignee_id')
        reviewer_id = data.get('reviewer_id')

        if assignee_id:
            if not board.members.filter(id=assignee_id).exists():
                raise serializers.ValidationError("Assignee must be a member of the board.")

        if reviewer_id:
            if not board.members.filter(id=reviewer_id).exists():
                raise serializers.ValidationError("Reviewer must be a member of the board.")

        return data

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)
        task = Tasks.objects.create(**validated_data)

        if assignee_id:
            task.assignee = User.objects.get(id=assignee_id)
        if reviewer_id:
            task.reviewer = User.objects.get(id=reviewer_id)

        task.save()
        return task
        
class TaskSerializerDetails(serializers.ModelSerializer):   
    assignee = MemberSerializer(read_only=True)  
    reviewer = MemberSerializer(read_only=True)
    
    
    class Meta:

        model = Tasks
        fields = '__all__'