import time

from game.actionlog_model import ActionLog
from game.ai import make_decision_and_move, take_path, move
from random import choice
from game.game_options import SLEEP_TIME

sleep_time = SLEEP_TIME


def repeat_move(character, target_x, target_y):
    while character.x != target_x or character.y != target_y:
        start_point, target_point = make_decision_and_move(character, target_x, target_y)
        if start_point is None or target_point is None:
            print("Invalid move decision.")
            break

        path = take_path(start_point, target_point)
        if path is not None:
            for point in path:
                move(character, point[0], point[1])
                if character.x == target_x and character.y == target_y:
                    print(f"Character {character.name} reached the target coordinates: ({target_x}, {target_y})")
                    action_description = choice(
                        open('game/text/travel/character_thoughts.txt').readlines()).format(
                        name=character.name,
                        x=target_x,
                        y=target_y,
                    )
                    ActionLog.objects.create(description=action_description, character=character)
                    time.sleep(sleep_time)
                    return
        else:
            print("No valid path found.")
            break

    print(f"Unable to reach the target coordinates: ({target_x}, {target_y})")
