from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=20)
    #member_count = models.ManyToManyField(User, related_name='board')
    members = models.ManyToManyField(User, related_name='boards')
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    tasks_high_prio_count = models.IntegerField(default=0)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards',default=1)
