from django.db import models


class Location(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default=None)
    passable = models.BooleanField(default=True)
