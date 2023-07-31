from django.db import models

from game.character_models import Character


class Animal(models.Model):
    name = models.CharField(max_length=100, default=None)
    age = models.IntegerField(default=0)
    species = models.CharField(max_length=100, default=None)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    health_max = models.IntegerField(default=100)
    stamina_max = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    regeneration = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    energy = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    intuition = models.IntegerField(default=10)
    luck = models.IntegerField(default=10)
    accuracy = models.IntegerField(default=10)
    experience = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    quest_character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)

    def speak(self):
        pass

    def eat(self):
        pass


class Dog(Animal):
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def speak(self):
        return "Woof!"

    def eat(self):
        return "The dog is eating."


class Cat(Animal):
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)

    def speak(self):
        return "Meow!"

    def eat(self):
        return "The cat is eating."
