from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True) # wird automatisch gesetzt , queryset=User.objects.all() das nur in der daten bank manuell eingeben
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
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)
    members_details = MemberSerializer(
        source='member_count', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'members_details',
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        if members is not None:
            instance.member_count.set(members)
            return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['members'] = rep.pop('members_details', [])

        return rep
