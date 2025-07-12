from django.urls import path
from .view import BoardListCreateView 

urlpatterns = [  
    path('boards/', BoardListCreateView.as_view(), name='board-list'), 
]
