from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer, BoardSerializerDetails
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .permissions import IsOwner

class BoardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = BoardSerializer

    def get_queryset(self):

        return Board.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):        
        members = self.request.data.get('members', [])       
        board = serializer.save(owner=self.request.user)
      
        if members:
            users = User.objects.filter(id__in=members)
            board.members.set(users)


class BorderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = Board.objects.all()
    serializer_class = BoardSerializerDetails

   