from django.urls import path
from .view import BoardListCreateView, BorderDetailView, TaskListCreateView, TaskDetailAPIView, CommentListCreateAPIView, CommentDestroyAPIView,ReviewingTasksView,AssignedTasksView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BorderDetailView.as_view(), name='board-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='tasks-list'),
    path('tasks/<int:task_id>/', TaskDetailAPIView.as_view(),
         name='task-detail-update'),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name='assign-list'),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name='review-list'),
    path('tasks/<int:task_id>/comments/',
         CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/',
         CommentDestroyAPIView.as_view(), name='comment-destroy'),
]
