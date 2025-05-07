from django.urls import path
from .view import BoardView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board'),
    
]