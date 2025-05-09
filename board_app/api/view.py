from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class BoardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = BoardSerializer

    def get_queryset(self):

        return Board.objects.filter(owner_id=self.request.user)
