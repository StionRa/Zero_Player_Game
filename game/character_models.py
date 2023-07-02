from django.contrib.auth.models import User
from django.db import models
import random

class Character(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    RACE_CHOICES = (
        ('Human', 'Human'),
        ('Elf', 'Elf'),
        ('Dwarf', 'Dwarf'),
        # Add more race choices as needed
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    race = models.CharField(max_length=255, choices=RACE_CHOICES)
    health_max = models.IntegerField(default=100)
    mana_max = models.IntegerField(default=100)
    mana = models.IntegerField(default=100)
    stamina_max = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    energy = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    regeneration = models.IntegerField(default=10)
    intuition = models.IntegerField(default=10)
    luck = models.IntegerField(default=10)
    accuracy = models.IntegerField(default=10)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def attack(self, target):
        damage = self.strength * 3 - target.defense * 0.2
        target.health -= int(damage)
