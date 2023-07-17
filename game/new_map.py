import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Zero_Player_Game.settings")
django.setup()

from game.location_model.location_model import Location
from game.location_model.map_generator import generate_map


def reset_map():
    Location.objects.all().delete()
    generate_map()
