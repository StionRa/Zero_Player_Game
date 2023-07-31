from random import choice
from game.actionlog_model import ActionLog


def new_character(character):
    if character.new_character:
        action_description = choice(
            open('game/text/start_journey/first_time.html').readlines()).format(
            name=character.name,
        )
        ActionLog.objects.create(description=action_description, character=character)
        character.new_character = False
        character.save()
    else:
        return
