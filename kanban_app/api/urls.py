from django.urls import path
from .view import BoardView, BoardCreateView 

urlpatterns = [  
    path('boards/', BoardView.as_view(), name='board-list'), 
]
