# Generated by Django 5.2 on 2025-05-09 18:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='member_count',
            field=models.ManyToManyField(related_name='board', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='board',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_boards', to=settings.AUTH_USER_MODEL),
        ),
    ]
