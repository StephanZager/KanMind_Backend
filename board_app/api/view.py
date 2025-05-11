from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer, BoardSerializerDetails
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class BoardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = BoardSerializer

    def get_queryset(self):

        return Board.objects.filter(owner_id=self.request.user)


class BorderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializerDetails

   