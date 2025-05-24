from django.urls import path
from .view import TasksView,AssignedToMeView,ReviewingView,TaskDetailView,CommentListCreateView,CommentDeleteView

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='tasks-details'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='tasks-reviewing'),
     path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view(), name='task-comment-delete'),
   # path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'),
    
]