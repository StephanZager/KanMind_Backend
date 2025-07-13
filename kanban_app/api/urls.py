from django.urls import path
from .view import BoardListCreateView, BorderDetailView 

urlpatterns = [  
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'), 
]
