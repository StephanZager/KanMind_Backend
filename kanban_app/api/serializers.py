from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board, Tasks, Comment


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializes a User object for member representation, including a custom 'fullname' field.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """Combines the user's first and last name into a single string."""
        return f"{obj.first_name} {obj.last_name}".strip()


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializes a Board object for list views, providing summary counts for
    members and tasks.
    """
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
        """Returns the total number of members on the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks on the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with the status 'to-do'."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks with 'high' priority."""
        return obj.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Handles the creation of a new Board, accepting a list of member IDs.
    """
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

class BoardUpdateSerializer(serializers.ModelSerializer):
   
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)

        if members_data is not None:
            instance.members.set(members_data)
        
        instance.save()
        return instance        

class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    """
    Formatiert die AUSGABE nach einer erfolgreichen PUT/PATCH-Anfrage.
    """
    owner_data = MemberSerializer(read_only=True, source='owner')
    members_data = MemberSerializer(many=True, read_only=True, source='members')

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']

class MembersField(serializers.PrimaryKeyRelatedField):
    """
    Custom field to represent a member relationship using the MemberSerializer
    for detailed output instead of just an ID.
    """
    def to_representation(self, value):
        return MemberSerializer(instance=value).data


class TaskSerializer(serializers.ModelSerializer):
    """
    General-purpose serializer for Task objects, providing nested representations
    for assignee and reviewer, and a count of associated comments.
    """
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Returns the total number of comments on the task."""
        return obj.comments.count()


class TaskInBoardSerializer(TaskSerializer):
    """
    A specialized TaskSerializer for nested use within BoardSerializerDetails.
    It omits the 'board' field to avoid redundancy.
    """
    class Meta(TaskSerializer.Meta):
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']


class BoardSerializerDetails(serializers.ModelSerializer):
    """
    Provides a detailed, nested representation of a single Board, including
    full member data and a list of all associated tasks.
    """
    owner_id = serializers.ReadOnlyField(source='owner.id')
    members = MembersField(many=True, queryset=User.objects.all())
    tasks = TaskInBoardSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Handles creating and updating tasks. Accepts user IDs for 'assignee' and
    'reviewer' and validates that they are members of the associated board.
    """
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
        """
        Ensures that the assignee and reviewer are members of the board.
        Note: This validation needs to be adjusted for updates where 'board'
        might not be in the data payload.
        """
        board = data.get('board') or (self.instance and self.instance.board)
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if not board:
             raise serializers.ValidationError("Board is required for validation.")

        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                "The assigned user is not a member of the board.")
        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                "The auditor is not a member of the board.")

        return data

    def create(self, validated_data):
        """Handles the creation of a new task instance."""
        return Tasks.objects.create(**validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Specifically handles updating an existing Task. The 'board' field is
    read-only to prevent moving a task to a different board.
    """
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
        """
        Validates that any new assignee or reviewer is a member of the
        task's existing board.
        """
        board = self.instance.board
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                {"assignee_id": "The assigned user is not a member of the board."}
            )

        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                {"reviewer_id": "The auditor is not a member of the board."}
            )

        return data


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Provides a detailed representation of a single Task, with nested data
    for the assignee and reviewer.
    """
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date']


class CommentSerializer(serializers.ModelSerializer):
    """
    Handles the serialization of Comment objects, showing the author's full name.
    """
    author = serializers.CharField(
        source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def validate_content(self, value):
        """Ensures the comment content is not empty."""
        if not value.strip():
            raise serializers.ValidationError(
                "The content cannot be empty.")
        return value

