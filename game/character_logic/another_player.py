import time
from random import choice

from game.actionlog_model import ActionLog
from game.battle.pvp_battle import battle_pvp
from game.character_models import Character
from game.models.town_model import City
from game.game_options import SLEEP_TIME

sleep_time = SLEEP_TIME

# Добавим словарь, который будет хранить информацию о том, что персонажи уже поприветствовали друг друга на
# определенной координате
greeted_characters = {}


def greet(character):
    target_x = character.x
    target_y = character.y
    other_character = Character.objects.filter(x=target_x, y=target_y).exclude(id=character.id).first()
    action_description = choice(
        open('game/text/travel/greet_character.txt').readlines()).format(
        name=character.name,
        other_character=other_character.name
    )
    time.sleep(sleep_time)
    ActionLog.objects.create(description=action_description, character=character)
    action_description_answer = choice(
        open('game/text/travel/greet_character_answer.txt').readlines()).format(
        name=character.name,
        other_character=other_character.name
    )
    ActionLog.objects.create(description=action_description_answer, character=character)
    time.sleep(sleep_time)

    # Добавляем информацию о приветствии персонажей на этой координате в словарь
    greeted_characters[(character.id, other_character.id)] = True


def initiate_battle(character):
    battle_pvp(character)
    time.sleep(sleep_time)


def make_choice_what_to_do(character):
    city = City.objects.filter(x_coordinate=character.x, y_coordinate=character.y).first()
    target_x = character.x
    target_y = character.y
    other_character = Character.objects.filter(x=target_x, y=target_y).exclude(id=character.id).first()
    if other_character and character.x == other_character.x and character.y == other_character.y:
        if city and other_character:
            greet(character)
            time.sleep(sleep_time)
        else:
            actions = [greet, initiate_battle]
            selected_actions = choice(actions)
            selected_actions(character)
            time.sleep(sleep_time)
    else:
        return
