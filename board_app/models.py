from django.db import models
from user_auth_app.models import UserProfile

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=20)
    member_count = models.ManyToManyField(UserProfile, related_name='board')
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    task_hight_prio_count = models.IntegerField(default=0)
    owner_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owned_boards')
