import game.game_options as opt
from game.map_renderer import get_cell_color
from django.db import models
from .location_model import Location
from game.animal_model import Animal

display_width = opt.PLAYER_WIDTH
display_height = opt.PLAYER_HEIGHT


def print_map(map_x, character_x_navi, character_y_navi):
    start_x = character_x_navi - display_width // 2
    start_y = character_y_navi - display_height // 2

    end_x = character_x_navi + display_width // 2
    end_y = character_y_navi + display_width // 2
    min_x = Location.objects.aggregate(models.Min('x'))['x__min']
    min_y = Location.objects.aggregate(models.Min('y'))['y__min']
    html_output = ""
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            animal = Animal.objects.filter(x=x, y=y).first()
            if x == character_x_navi and y == character_y_navi:
                symbol = '@'
            elif animal:
                symbol = '='
            else:
                if x >= min_x and y >= min_y:  # Добавляем проверку на положительные координаты
                    cell = map_x[y][x]
                    if cell is None:
                        symbol = 'X'
                    elif cell:
                        symbol = '.'
                    else:
                        symbol = '#'
                else:
                    symbol = 'X'  # Используем символ 'X' для отображения недопустимых координат

            cell_color = get_cell_color(symbol)
            html_output += f"<div class='map-location' style='background-color: {cell_color};'></div>"
    return html_output
