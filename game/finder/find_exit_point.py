import random

from game.location_model.location_model import Location


def find_exit_point(city):
    adjacent_coordinates = [
        (city.x_coordinate + 1, city.y_coordinate),
        (city.x_coordinate - 1, city.y_coordinate),
        (city.x_coordinate, city.y_coordinate + 1),
        (city.x_coordinate, city.y_coordinate - 1)
    ]

    random.shuffle(adjacent_coordinates)

    for coordinate in adjacent_coordinates:
        location = Location.objects.filter(x=coordinate[0], y=coordinate[1]).first()
        if location and location.passable:
            return coordinate

    return None
