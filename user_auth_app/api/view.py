from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class RegistrationView(APIView):
    
        
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
       
        data={}
        if serializer.is_valid():
            save_account = serializer.save()
            token, created = Token.objects.get_or_create(user=save_account)
            data = {
                'token': token.key,
                'username': save_account.username,
                'email': save_account.email,
            }
        else:
            data=serializer.errors
        
        return Response(data)        
            


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
   