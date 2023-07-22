# faq/models.py

from django.db import models
from game.models.town_model import City
from game.game_items.item_model import Item, ItemCategory


class GameInfo(models.Model):
    title = models.CharField(max_length=100, unique=True)
    min_description = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


class WorldInfo(models.Model):
    game_info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class FAQTown(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    faq_name = models.CharField(max_length=100)
    faq_category = models.CharField(max_length=100)
    faq_description = models.TextField()

    def __str__(self):
        return self.faq_name


class FAQItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    faq_title = models.CharField(max_length=100)
    fiq_item_category = models.CharField(max_length=100)
    faq_description = models.TextField()

    def __str__(self):
        return self.faq_title


class FAQItemCategory(models.Model):
    item_category = models.OneToOneField(ItemCategory, on_delete=models.CASCADE)
    faq_title = models.CharField(max_length=100)
    faq_description = models.TextField()
