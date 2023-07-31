import time

from game.location_model.location_model import Location
from game.actionlog_model import ActionLog
from game.pathfinding import a_star_search
from random import choice
from game.game_options import SLEEP_TIME, CHARACTER_COST_STEP

sleep_time = SLEEP_TIME
step = CHARACTER_COST_STEP


def move(character, target_x, target_y):
    target_cell = Location.objects.filter(x=target_x, y=target_y, passable=True).first()
    if target_cell:
        character.x = target_x
        character.y = target_y
        character.stamina = max(character.stamina - step, 0)
        character.save()
        action_description = choice(open('game/text/travel/travel.xml').readlines()).format(
            name=character.name,
            x=target_x,
            y=target_y,
        )
        ActionLog.objects.create(description=action_description, character=character)
        print(f"Character {character.name} moved to coordinates: ({target_x}, {target_y})")
        time.sleep(sleep_time)
    else:
        print(f"The cell at coordinates ({target_x}, {target_y}) is impassable or does not exist.")


def handle_reached_target():
    print("Reached the target!")


def make_decision_and_move(character, target_x, target_y):
    current_cell = Location.objects.get(x=character.x, y=character.y)
    if target_x == current_cell.x and target_y == current_cell.y:
        handle_reached_target()
        return None, None
    elif target_x != current_cell.x or target_y != current_cell.y:
        start_point = current_cell.x, current_cell.y
        target_point = target_x, target_y

        print(f"Character {character.name} making a move decision from ({current_cell.x}, {current_cell.y}) "
              f"to ({target_x}, {target_y})")
        return start_point, target_point


def take_path(start_point, target_point):
    path = a_star_search(start_point, target_point)
    if path is None:
        print(f"No path found from {start_point} to {target_point}")
    else:
        print(f"Path found from {start_point} to {target_point}: {path}")
    return path
