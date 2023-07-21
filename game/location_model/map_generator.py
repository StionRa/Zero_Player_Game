from game.location_model.location_model import Location
from django.db import models
import random
import game.game_options as opt
from game import game_options
from game.models.create_city import create_sample_city

width = opt.WIDTH
height = opt.HEIGHT
min_temperature = game_options.MIN_TEMPERATURE
max_temperature = game_options.MAX_TEMPERATURE

global_min_x = Location.objects.aggregate(models.Min('x'))['x__min']
global_max_x = Location.objects.aggregate(models.Max('x'))['x__max']
global_min_y = Location.objects.aggregate(models.Min('y'))['y__min']
global_max_y = Location.objects.aggregate(models.Max('y'))['y__max']

map_created = False


def map_exists():
    return Location.objects.exists()


def generate_map():
    map_data_generate = []
    for y in range(-height, height):
        row = []
        for x in range(-width, width):
            name = f"{x},{y}"
            passable = random.choices([True, False], weights=[17, 3])[0]
            temperature = random.uniform(min_temperature, max_temperature)
            location = Location(x=x, y=y, name=name, passable=passable, temperature=temperature)
            row.append(location)
        map_data_generate.extend(row)

    Location.objects.bulk_create(map_data_generate)
    generate_river()
    generate_lake()
    create_sample_city()


def generate_river():
    global global_min_x, global_min_y, global_max_x, global_max_y

    river_start_x = global_min_x
    river_end_x = global_max_x

    # Начало реки
    river_start_y = random.randint(global_min_y, global_max_y)

    # Случайное извилистое течение реки
    river_path = [river_start_y]
    for _ in range(river_start_x + 1, river_end_x):
        prev_y = river_path[-1]
        next_y = random.randint(prev_y - 1, prev_y + 1)
        next_y = max(global_min_y, min(global_max_y, next_y))  # Ограничение по границам карты
        river_path.append(next_y)

    # Установка флага river для локаций, принадлежащих реке
    for x, y in zip(range(river_start_x, river_end_x + 1), river_path):
        location = Location.objects.get(x=x, y=y)
        location.river = True
        location.save()


def generate_lake():
    global global_min_x, global_min_y, global_max_x, global_max_y

    # Случайные координаты озера
    lake_x = random.randint(global_min_x, global_max_x)
    lake_y = random.randint(global_min_y, global_max_y)

    # Размеры озера (высота и ширина)
    lake_width = random.randint(1, 3)
    lake_height = random.randint(1, 3)

    # Установка флага lake для локаций, принадлежащих озеру
    for x in range(lake_x, lake_x + lake_width):
        for y in range(lake_y, lake_y + lake_height):
            if global_min_x <= x <= global_max_x and global_min_y <= y <= global_max_y:
                location = Location.objects.get(x=x, y=y)
                location.lake = True
                location.save()


def load_map():
    global global_min_x, global_min_y, global_max_x, global_max_y, map_created
    if not map_exists():
        map_created = False
        return generate_map()
    map_data = Location.objects.values_list('x', 'y', 'passable', 'temperature', 'river', 'lake')

    if map_data:
        x_values, y_values, passables, temperatures, rivers, lakes = zip(*map_data)
        width_x = max(max(x_values) + 1, width)
        height_y = max(max(y_values) + 1, height)

        map_load = [[True for _ in range(width_x)] for _ in range(height_y)]
        temperature_map = [[True for _ in range(width_x)] for _ in range(height_y)]
        river_map = [[True for _ in range(width_x)] for _ in range(height_y)]
        lake_map = [[True for _ in range(width_x)] for _ in range(height_y)]

        for x, y, passable, temperature, river, lake in zip(x_values, y_values, passables, temperatures, rivers, lakes):
            map_load[y][x] = passable
            temperature_map[y][x] = temperature
            river_map[y][x] = river
            lake_map[y][x] = lake

        global_min_x = min(x_values)
        global_min_y = min(y_values)
        global_max_x = max(x_values)
        global_max_y = max(y_values)

        return map_load, temperature_map, river_map, lake_map
