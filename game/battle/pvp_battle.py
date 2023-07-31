import time

from game.actionlog_model import ActionLog
from game.battle.character_dead import character_dead
from game.character_models import Character
from game.game_options import SLEEP_TIME, CHARACTER_COST_BATTLE_PVP
from game.battle.atack_standart import attack
sleep_time = SLEEP_TIME
cost = CHARACTER_COST_BATTLE_PVP


def battle_pvp(character):
    # Проверяем, есть ли другой персонаж на указанных координатах
    target_x = character.x
    target_y = character.y
    other_character = Character.objects.filter(x=target_x, y=target_y).exclude(id=character.id).first()
    if other_character:
        # Персонаж встретил другого персонажа
        action_description = f"{character.name} встретил {other_character.name} на координатах ({target_x}, {target_y})"
        ActionLog.objects.create(description=action_description, character=character)
        time.sleep(sleep_time)
        # Битва между персонажами
        while character.health > 0 and other_character.health > 0:
            # Персонаж атакует другого персонажа
            # character.attack(other_character)
            attack(character, other_character, character)
            # action_description = f"{character.name} атаковал {other_character.name}, здоровье " \
            #                      f"{other_character.health}/{other_character.health_max}"
            # ActionLog.objects.create(description=action_description, character=character)

            # Проверка условия окончания битвы
            if other_character.health <= 0:
                action_description = f"{other_character.name} был повержен"
                ActionLog.objects.create(description=action_description, character=character)
                # Обработка победы персонажа
                character.pvp_battle += 1
                character.experience += (other_character.level + character.luck) * 8
                character.stamina = max(character.stamina - cost, 0)
                character_dead(other_character)
                time.sleep(sleep_time)
                break

            # Другой персонаж атакует первого персонажа
            # other_character.attack(character)
            attack(other_character, character, character)
            # action_description = f"{other_character.name} атаковал {character.name}, здоровье " \
            #                      f"{character.health}/{character.health_max}"
            # ActionLog.objects.create(description=action_description, character=character)

            # Проверка условия окончания битвы
            if character.health <= 0:
                action_description = f"{character.name} был повержен"
                ActionLog.objects.create(description=action_description, character=character)
                # Обработка победы другого персонажа
                other_character.pvp_battle += 1
                other_character.experience += (character.level + other_character.luck) * 8
                character.stamina = max(character.stamina - cost, 0)
                character_dead(character)
                time.sleep(sleep_time)
                break
