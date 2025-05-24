from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User
from task_app.api.serializers import TasksSerializer

class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(source='owner.id', read_only=True)
    member_count = serializers.SerializerMethodField()
    

    class Meta:

        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
    
    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()    


class BoardSerializerDetails(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )

    # Zum Lesen: Ausgabe als User-Objekte
    members_details = MemberSerializer(
        source='members', many=True, read_only=True
    )
    tasks = TasksSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'members_details',
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count','tasks']

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        if members is not None:
            instance.members.set(members)
            return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['members'] = rep.pop('members_details', [])

        return rep
