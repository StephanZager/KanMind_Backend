from rest_framework import generics
from board_app.models import Board
from .serializers import BoardSerializer

class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer