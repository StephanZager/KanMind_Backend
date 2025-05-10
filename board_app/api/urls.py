from django.urls import path
from .view import BoardView,BorderDetailView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board'),
    path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'),
    
]