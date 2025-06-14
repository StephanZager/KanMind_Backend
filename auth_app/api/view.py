from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class ResgistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            save_account = serializer.save()
            token = Token.objects.get_or_create(user=save_account)
            data = {
                'token': token.key,
                'username': save_account.username,
                'email': save_account.email
            }
        else:
            data = serializer.errors

        return Response(data)
