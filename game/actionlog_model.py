from django.db import models
from game.character_models import Character


class ActionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
