from .location_model import Location
import random
import game.game_options as opt

width = opt.WIDTH
height = opt.HEIGHT


def check_map_existence():
    map_exists = Location.objects.exists()
    return map_exists


def generate_map():
    map_data_generate = []
    for y in range(height):
        row = []
        for x in range(width):
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
        min_y = 0
        max_y = height - 1
        new_width = width + part_width
        new_height = height
    elif direction == 'right':
        min_x = width
        max_x = width + part_width - 1
        min_y = 0
        max_y = height - 1
        new_width = width + part_width
        new_height = height
    elif direction == 'top':
        min_x = 0
        max_x = width - 1
        min_y = -part_height
        max_y = -1
        new_width = width
        new_height = height + part_height
    elif direction == 'bottom':
        min_x = 0
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
    global height, width
    map_data = Location.objects.all()

    location_data = [(location.x, location.y, location.passable) for location in map_data]
    if location_data:
        x_values, y_values, _ = zip(*location_data)
        width = max(max(x_values) + 1, width)
        height = max(max(y_values) + 1, height)

    map_load = [[True for _ in range(width)] for _ in range(height)]
    for x, y, passable in location_data:
        map_load[y][x] = passable

    return map_load
