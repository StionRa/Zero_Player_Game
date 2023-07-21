import game.game_options as opt
from game.location_model.map_renderer import get_cell_color
from django.db import models
from game.location_model.location_model import Location
from game.animal.animal_model import Animal
from game.models.town_model import City
from game.character_models import Character

display_width = opt.PLAYER_WIDTH
display_height = opt.PLAYER_HEIGHT


def print_map(map_x, river_map, lake_map, character_x_navi, character_y_navi):
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
            citys = City.objects.filter(x_coordinate=x, y_coordinate=y).first()
            character = Character.objects.filter(x=x, y=y).first()
            if x == character_x_navi and y == character_y_navi:
                symbol = '@'
            elif character:
                symbol = 'C'
            elif animal:
                symbol = 'A'
            elif citys:
                symbol = '%'
            else:
                if x >= min_x and y >= min_y:
                    try:
                        cell = map_x[y][x]
                        if cell is None:
                            symbol = 'X'
                        elif cell:
                            symbol = '.'
                        else:
                            symbol = '#'
                        if river_map[y][x]:
                            symbol = '~'  # Обозначение реки
                        elif lake_map[y][x]:
                            symbol = 'O'  # Обозначение озера
                    except IndexError:
                        symbol = 'X'  # Handle missing coordinates with 'X'

                else:
                    symbol = 'X'  # Use 'X' to represent invalid coordinates

            cell_color = get_cell_color(symbol)
            html_output += f"<div class='map-location' style='background-color: {cell_color};'>{symbol}</div>"

    return html_output
