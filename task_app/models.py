from django.db import models
from django.contrib.auth.models import User
from board_app.models import Board


class Tasks(models.Model):
    
    STATUS_CHOICES = [
        ('to-do', 'To-Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_tasks')
    due_date = models.DateField()
    
class Comment(models.Model):
    task = models.ForeignKey('Tasks', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    