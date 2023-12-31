from django.db import models


class Location(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default=None)
    passable = models.BooleanField(default=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    river = models.BooleanField(default=False)
    lake = models.BooleanField(default=False)
