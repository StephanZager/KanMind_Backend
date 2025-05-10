from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    member_count = serializers.SerializerMethodField()

    class Meta:

        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.member_count.count()


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class BoardSerializerDetails(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        members = obj.member_count.all()
        return MemberSerializer(members, many=True).data
