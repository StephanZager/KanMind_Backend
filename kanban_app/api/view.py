from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, BoardCreateSerializer
from django.contrib.auth.models import User
from .permissions import IsOwner, IsMember
from models import Board


class BoardView(generics.ListAPIView):

    queryset = Board.object.all()
    permission_classes = [IsAuthenticated, IsOwner | IsMember]
    serializer_class = BoardSerializer


class BoardCreateView(generics.CreateAPIView):

    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
