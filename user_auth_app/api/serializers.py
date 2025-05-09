from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'pw does not agree'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': 'A user with this email already exists'})

        user_account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        user_account.set_password(pw)
        user_account.save()

        return user_account


class UserProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
