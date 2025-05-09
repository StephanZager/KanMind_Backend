from rest_framework import serializers
from board_app.models import Board
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    owner_id= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    member_count = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:

        model = Board
        fields = '__all__'
        
        
    def get_member_count(self, obj):
        
        return obj.member_count.count()

