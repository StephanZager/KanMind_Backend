from rest_framework import serializers
from board_app.models import Board
from user_auth_app.models import UserProfile
from user_auth_app.api.serializers import UserProfileSerializer


class BoardSerializer(serializers.ModelSerializer):
    owner_id= serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    member_count = serializers.SerializerMethodField()

    class Meta:

        model = Board
        fields = '__all__'
        
    def get_member_count(self, obj):
        
        return obj.member_count.count()

