from game.actionlog_model import ActionLog
from game.finder.nearest_city_find import find_nearest_city


def character_dead(character):
    target_x, target_y = find_nearest_city(character)
    if target_x is None or target_y is None:
        pass
    else:
        character.x = target_x
        character.y = target_y
        character.save()
        action_description = f"{character.name} был перенесен в координаты ({character.x}, " \
                             f"{character.y})"
        ActionLog.objects.create(description=action_description, character=character)
