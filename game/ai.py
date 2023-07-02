# ai.py
from game.location_model import Location
from game.actionlog_model import ActionLog
from game.pathfinding import a_star_search
from random import choice


def move(character, target_x, target_y):
    target_cell = Location.objects.filter(x=target_x, y=target_y, passable=True).first()
    if target_cell:
        character.x = target_x
        character.y = target_y
        character.save()
        action_description = choice(open('game/text/travel/travel.txt').readlines()).format(
            name=character.name,
            x=target_x,
            y=target_y,
        )
        ActionLog.objects.create(description=action_description, character=character)
    else:
        print(f"Ячейка с координатами ({target_x}, {target_y}) не проходима или не существует.")


def handle_reached_target():
    print("Вы достигли цели!!!")


def make_decision_and_move(character, target_x, target_y):
    current_cell = Location.objects.get(x=character.x, y=character.y)
    if target_x == current_cell.x and target_y == current_cell.y:
        handle_reached_target()
    elif target_x != current_cell.x or target_y != current_cell.y:
        start_point = current_cell.x, current_cell.y
        target_point = target_x, target_y

        return start_point, target_point


def take_path(start_point, target_point):
    path = a_star_search(start_point, target_point)
    return path
