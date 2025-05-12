from django.urls import path
from .view import TasksView

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
   # path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'),
    
]