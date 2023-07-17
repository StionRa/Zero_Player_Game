from game.ai import take_path
from game.models.town_model import City


def find_nearest_city(character):
    cities = City.objects.all()
    print('find all city`s:', cities)
    if cities:
        start = (character.x, character.y)
        target_cities = [(city.x_coordinate, city.y_coordinate) for city in cities]
        paths = []
        for target in target_cities:
            path = take_path(start, target)
            if path:
                paths.append((target, path))
        if paths:
            nearest_target, nearest_path = min(paths, key=lambda p: len(p[1]))
            nearest_x, nearest_y = nearest_target[0], nearest_target[1]
            print("Nearest city found at coordinates:", nearest_x, nearest_y)
            return nearest_x, nearest_y
    print("No cities found.")
    return None, None
