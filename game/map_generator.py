from game.location_model import Location
from django.db import models
import random
import game.game_options as opt

width = opt.WIDTH
height = opt.HEIGHT

global_min_x = Location.objects.aggregate(models.Min('x'))['x__min']
global_max_x = Location.objects.aggregate(models.Max('x'))['x__max']
global_min_y = Location.objects.aggregate(models.Min('y'))['y__min']
global_max_y = Location.objects.aggregate(models.Max('y'))['y__max']
map_created = False


def map_exists():
    return Location.objects.exists()


def generate_map():
    global map_created
    if map_exists():
        map_created = True
        return
    map_data_generate = []
    for y in range(-height, height):
        row = []
        for x in range(-width, width):
            name = f"{x},{y}"
            passable = random.choices([True, False], weights=[17, 3])[0]
            location = Location(x=x, y=y, name=name, passable=passable)
            row.append(location)
        map_data_generate.extend(row)

    Location.objects.bulk_create(map_data_generate)
    map_created = True


def load_map():
    global global_min_x, global_min_y, global_max_x, global_max_y, map_created
    if not map_exists():
        map_created = False
        return generate_map()
    map_data = Location.objects.values_list('x', 'y', 'passable')

    if map_data:
        x_values, y_values, _ = zip(*map_data)
        width_x = max(max(x_values) + 1, width)
        height_y = max(max(y_values) + 1, height)

        map_load = [[True for _ in range(width_x)] for _ in range(height_y)]

        for x, y, passable in map_data:
            map_load[y][x] = passable

        global_min_x = min(x_values)
        global_min_y = min(y_values)
        global_max_x = max(x_values)
        global_max_y = max(y_values)

        return map_load
