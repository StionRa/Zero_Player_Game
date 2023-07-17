from django.db import models
from game.character_models import Character


class Quest(models.Model):
    model_task = (
        ('k', 'kill_animal'),
        ('f', 'find'),
    )
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='quests')
    name = models.CharField(max_length=255)
    description = models.TextField()
    task_model = models.CharField(max_length=100, choices=model_task)
    completed = models.BooleanField(default=False)
    experience_reward = models.IntegerField(default=0)
    objective_quantity = models.PositiveIntegerField(default=0)
    objective_progress = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

        # Additional logic for quest completion, if needed
        # You can update other game objects or perform specific actions here
