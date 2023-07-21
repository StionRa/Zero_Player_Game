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
    experience = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    quest_character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)

    def speak(self):
        pass

    def eat(self):
        pass

    def attack(self, target):
        damage = self.strength * 3 - target.defense * 0.2
        target.health -= int(damage)
        if target.health <= 0:
            # Check if the target is a Character (subclass of Animal) and update quest_character accordingly
            self.quest_character = None
            self.health = self.health_max  # Reset the animal's health to full
            self.age += 1
        self.save()
        target.save()


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
