from celery import shared_task
from .ai import make_decision_and_move, take_path, move
from .character_models import Character
from time import sleep
from game.location_model import Location


@shared_task
def update_character_state():
    sleep(5)
    characters = Character.objects.all()
    for character in characters:
        # Здесь можешь задать целевые координаты для персонажа, например, с помощью случайных значений
        target_x = 5
        target_y = 8
        start_point = make_decision_and_move(character, target_x, target_y)[0]
        target_point = make_decision_and_move(character, target_x, target_y)[1]
        path = take_path(start_point, target_point)
        if path is not None:
            print(path)
            for point in path:
                location = Location.objects.get(x=point[0], y=point[1])
                if location.passable:
                    move(character, point[0], point[1])
                    sleep(5)
        else:
            print("Невозможно найти допустимый путь к цели.")
    else:
        print("Недопустимые координаты цели.")
