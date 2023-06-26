from .location_model import Location
from django.db import models
import random
import game.game_options as opt

width = opt.WIDTH
height = opt.HEIGHT


def check_map_existence():
    map_exists = Location.objects.exists()
    return map_exists


# def generate_map():
#     map_data_generate = []
#     for y in range(height):
#         row = []
#         for x in range(width):
#             name = f"{x},{y}"
#             passable = random.choices([True, False], weights=[17, 3])[0]
#             location = Location(x=x, y=y, name=name, passable=passable)
#             row.append(location)
#         map_data_generate.extend(row)
#
#     Location.objects.bulk_create(map_data_generate)
#
#
# def add_map_part(part_width, part_height, direction):
#     global width, height
#     if direction == 'left':
#         min_x = -part_width
#         max_x = -1
#         min_y = 0
#         max_y = height - 1
#         new_width = width + part_width
#         new_height = height
#     elif direction == 'right':
#         min_x = width
#         max_x = width + part_width - 1
#         min_y = 0
#         max_y = height - 1
#         new_width = width + part_width
#         new_height = height
#     elif direction == 'top':
#         min_x = 0
#         max_x = width - 1
#         min_y = -part_height
#         max_y = -1
#         new_width = width
#         new_height = height + part_height
#     elif direction == 'bottom':
#         min_x = 0
#         max_x = width - 1
#         min_y = height
#         max_y = height + part_height - 1
#         new_width = width
#         new_height = height + part_height
#     else:
#         raise ValueError("Invalid direction. Allowed values: 'left', 'right', 'top', 'bottom'.")
#
#     new_part = [Location(x=x, y=y, name=f"{x},{y}", passable=random.choices([True, False], weights=[17, 3])[0])
#                 for y in range(min_y, max_y + 1)
#                 for x in range(min_x, max_x + 1)]
#
#     Location.objects.bulk_create(new_part)
#
#     width = new_width
#     height = new_height


def generate_map():
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


def add_map_part(part_width, part_height, direction):
    global width, height
    if direction == 'left':
        min_x = -part_width
        max_x = -1
        min_y = -height
        max_y = height - 1
        new_width = width + part_width
        new_height = height
    elif direction == 'right':
        min_x = width
        max_x = width + part_width - 1
        min_y = -height
        max_y = height - 1
        new_width = width + part_width
        new_height = height
    elif direction == 'top':
        min_x = -width
        max_x = width - 1
        min_y = -part_height
        max_y = -1
        new_width = width
        new_height = height + part_height
    elif direction == 'bottom':
        min_x = -width
        max_x = width - 1
        min_y = height
        max_y = height + part_height - 1
        new_width = width
        new_height = height + part_height
    else:
        raise ValueError("Invalid direction. Allowed values: 'left', 'right', 'top', 'bottom'.")

    new_part = [Location(x=x, y=y, name=f"{x},{y}", passable=random.choices([True, False], weights=[17, 3])[0])
                for y in range(min_y, max_y + 1)
                for x in range(min_x, max_x + 1)]

    Location.objects.bulk_create(new_part)

    width = new_width
    height = new_height


def load_map():
    min_x = Location.objects.aggregate(models.Min('x'))['x__min']
    max_x = Location.objects.aggregate(models.Max('x'))['x__max']
    min_y = Location.objects.aggregate(models.Min('y'))['y__min']
    max_y = Location.objects.aggregate(models.Max('y'))['y__max']
    width_load = max_x - min_x
    height_load = max_y - min_y
    map_data = Location.objects.values_list('x', 'y', 'passable')

    if map_data:
        x_values, y_values, _ = zip(*map_data)
        width_x = max(max(x_values) + 1, width_load)
        height_y = max(max(y_values) + 1, height_load)

        map_load = [[True for _ in range(width_x)] for _ in range(height_y)]

        for x, y, passable in map_data:
            map_load[y][x] = passable

        return map_load


def check_and_extend_map(character_x, character_y):
    # Получаем минимальные и максимальные значения координат из базы данных
    min_x = Location.objects.aggregate(models.Min('x'))['x__min']
    max_x = Location.objects.aggregate(models.Max('x'))['x__max']
    min_y = Location.objects.aggregate(models.Min('y'))['y__min']
    max_y = Location.objects.aggregate(models.Max('y'))['y__max']

    # Проверяем, достиг ли персонаж края карты

    # Проверка левого края карты
    if character_x == min_x:
        add_map_part(width, height, 'left')
        character_x += width

    # Проверка правого края карты
    if character_x == max_x:
        add_map_part(width, height, 'right')

    # Проверка верхнего края карты
    if character_y == min_y:
        add_map_part(width, height, 'top')
        character_y += height

    # Проверка нижнего края карты
    if character_y == max_y:
        add_map_part(width, height, 'bottom')

    return character_x, character_y
