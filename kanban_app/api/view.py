from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, BoardCreateSerializer,BoardSerializerDetails
from django.contrib.auth.models import User
from .permissions import IsOwner, IsMember
from ..models import Board
from django.db.models import Q


class BoardListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BorderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,IsOwner | IsMember]
    queryset = Board.objects.all()
    serializer_class = BoardSerializerDetails