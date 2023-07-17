from game.models.city_logic import enter_city
from game.finder.nearest_city_find import find_nearest_city
from game.movement.repeat_move_to_target import repeat_move


def back_to_city(character):
    target_x, target_y = find_nearest_city(character)
    print('search for nearest city 2')
    if target_x is None or target_y is None:
        pass
    elif character.x == target_x and character.y == target_y:
        print("Already at the nearest city. 2")
        enter_city(character)  # Запустить задачу enter_city_task с аргументом character
    else:
        print('repeat move to nearest city 2')
        repeat_move(character, target_x, target_y)
