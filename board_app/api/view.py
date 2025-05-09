from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class BoardView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
   # queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
    def get_queryset(self):
        # Zeige nur Boards an, die dem angemeldeten Benutzer gehören
        return Board.objects.filter(owner_id=self.request.user)
    
    #def perform_create(self, serializer):
    #    owner_id = serializer.validated_data.get('owner_id')
    #    if not User.objects.filter(id=owner_id.id).exists():
    #        raise ValidationError({'owner_id': 'Der angegebene Benutzer existiert nicht.'})
    #    serializer.save()