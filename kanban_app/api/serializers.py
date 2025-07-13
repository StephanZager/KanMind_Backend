from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner.id', read_only=True)
    member_count = serializers.SerializerMethodField(default=0)
    ticket_count = serializers.SerializerMethodField(default=0)
    tasks_to_do_count = serializers.SerializerMethodField(default=0)
    tasks_high_prio_count = serializers.SerializerMethodField(default=0)

    class Meta:

        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        pass
        # return obj.tickets.count()

    def get_tasks_to_do_count(self, obj):
        pass
        # return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        pass
        # return obj.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']


class BoardSerializerDetails(serializers.ModelSerializer):
    members = MemberSerializer(
         many=True, read_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class TasksSerializer(serializers.ModelSerializer):
    pass


class TaskSerializerDetails(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
