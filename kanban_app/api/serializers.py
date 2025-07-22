from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board, Tasks


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


class MembersField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return MemberSerializer(instance=value).data


class TaskSerializer(serializers.ModelSerializer):
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskInBoardSerializer(TaskSerializer):

    class Meta(TaskSerializer.Meta):
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']


class BoardSerializerDetails(serializers.ModelSerializer):
    members = MembersField(many=True, queryset=User.objects.all())
    tasks = TaskInBoardSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Tasks
        fields = ['board', 'title', 'description', 'status', 'priority',
                  'assignee_id', 'reviewer_id', 'due_date']

    def validate(self, data):
        board = data.get('board')
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                "Der zugewiesene Benutzer ist kein Mitglied des Boards.")
        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                "Der Prüfer ist kein Mitglied des Boards.")

        return data

    def create(self, validated_data):

        assignee_obj = validated_data.pop('assignee', None)
        reviewer_obj = validated_data.pop('reviewer', None)

        task = Tasks.objects.create(**validated_data)

        task.assignee = assignee_obj
        task.reviewer = reviewer_obj
        task.save()

        return task


class TaskUpdateSerializer(serializers.ModelSerializer):

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'status', 'priority',
                  'assignee_id', 'reviewer_id', 'due_date', 'board']

        read_only_fields = ['board']

    def validate(self, data):

        board = self.instance.board

        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                {"assignee_id": "Der zugewiesene Benutzer ist kein Mitglied des Boards."}
            )

        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                {"reviewer_id": "Der Prüfer ist kein Mitglied des Boards."}
            )

        return data


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date']


class CommentSerializer(serializers.ModelSerializer):
    pass
