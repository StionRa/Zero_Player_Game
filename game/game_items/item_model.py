from django.db import models


# Модель категории предметов
class ItemCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Модель предмета
class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
