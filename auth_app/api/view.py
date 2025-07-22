from .serializers import RegistrationSerializer, EmailAuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User


class RegistrationView(APIView):
    """
    API view for user registration.

    Handles POST requests to create a new user account.
    Validates user data using RegistrationSerializer, creates the user and an auth token,
    and returns user information along with the token upon successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            save_account = serializer.save()
            token, created = Token.objects.get_or_create(user=save_account)
            data = {
                'token': token.key,
                'fullname': save_account.username,
                'email': save_account.email,
                'user_id': save_account.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    """
    API view for user login.

    Handles POST requests to authenticate a user with email and password.
    Uses a custom serializer to validate credentials and returns an auth token
    and user data upon successful authentication.
    """
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        fullname = f"{user.first_name} {user.last_name}".strip()

        return Response({
            'token': token.key,
            'fullname': fullname,
            'email': user.email,
            'user_id': user.id,
        })

class EmailCheckView(APIView):
    """
    API view to check if an email address is already registered.

    Handles GET requests with an 'email' query parameter.
    Returns the user's data if the email exists, otherwise returns a 404 Not Found error.
    """
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'detail': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            fullname = f"{user.first_name} {user.last_name}".strip()
            return Response({
                'id': user.id,
                'email': user.email,
                'fullname': fullname
            })
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class UserListView(APIView):
    """
    API view to list all registered users.

    Handles GET requests to retrieve a complete list of all users in the system,
    including their ID, email, and full name.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        user_list = [
            {
                'id': user.id,
                'email': user.email,
                'fullname': f"{user.first_name} {user.last_name}".strip(),
                'username': user.username,
            }
            for user in users
        ]
        return Response(user_list, status=status.HTTP_200_OK)      