from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner.id', read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()

    class Meta:

        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tickets.count()


class BoardSerializerDetails(serializers.ModelSerializer):
    pass


class TasksSerializer(serializers.ModelSerializer):
    pass


class TaskSerializerDetails(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
