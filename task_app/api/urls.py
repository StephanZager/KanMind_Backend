from django.urls import path
from .view import TasksView,AssignedToMeView,ReviewingView

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='tasks-reviewing'),
   # path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'),
    
]