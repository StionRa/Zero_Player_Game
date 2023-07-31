import time
from random import choice

from game.actionlog_model import ActionLog
from game.animal.animal_inventory import AnimalInventory
from game.battle.character_dead import character_dead
from game.quest.check_quest_completion import check_quest_completion
from game.game_options import SLEEP_TIME, CHARACTER_COST_BATTLE_WITH_ANIMAL
from game.battle.atack_standart import attack

sleep_time = SLEEP_TIME / 2
cost = CHARACTER_COST_BATTLE_WITH_ANIMAL


def get_or_create_animal_inventory(animal):
    try:
        return animal.animalinventory
    except AnimalInventory.DoesNotExist:
        # If AnimalInventory does not exist, create one
        animal_inventory = AnimalInventory.objects.create(animal=animal)
        return animal_inventory


def battle_with_animal(character, animal, quest, target_x, target_y):
    action_description = choice(open('game/text/battle/battle_start.xml').readlines()).format(
        name=character.name,
        species=animal.species,
        animal=animal.name,
        x=target_x,
        y=target_y,
        animal_health=animal.health,
        character_health=character.health
    )
    ActionLog.objects.create(description=action_description, character=character)
    animal_inventory = get_or_create_animal_inventory(animal)
    animal_inventory.generate_loot()
    animal_inventory.save()
    # Битва между персонажем и животным
    while character.health > 0 and animal.health > 0:
        attack(character, animal, character)
        if animal.health <= 0:
            action_description_lose = choice(
                open('game/text/battle/animal_lose_battle.xml').readlines()).format(
                name=character.name,
                species=animal.species,
                animal=animal.name,
                x=target_x,
                y=target_y,
                animal_health=animal.health,
                character_health=character.health
            )
            ActionLog.objects.create(description=action_description_lose, character=character)
            # Удаление животного из базы данных
            if animal.animalinventory:
                animal.animalinventory.transfer_items_to_character(character)
            character.experience += animal.experience
            quest.objective_progress += 1  # Increment the objective progress
            character.stamina = max(character.stamina - cost, 0)
            character.save()
            quest.save()
            animal.is_active = False
            animal.save()
            animal.delete()
            check_quest_completion(character)  # Check if the quest is completed
            break
        time.sleep(sleep_time)
        # Животное атакует
        attack(animal, character, character)
        time.sleep(sleep_time)
        # Проверка условия окончания битвы
        if character.health <= 0:
            # Персонаж проиграл
            action_description_lose = choice(
                open('game/text/battle/character_lose_battle.xml').readlines()).format(
                name=character.name,
                species=animal.species,
                animal=animal.name,
                x=target_x,
                y=target_y,
                animal_health=animal.health,
                character_health=character.health
            )
            ActionLog.objects.create(description=action_description_lose, character=character)
            # Перенос персонажа в ближайший город
            animal.is_active = True
            animal.quest_character = None
            animal.save()
            character.stamina = max(character.stamina - cost, 0)
            character_dead(character)
            break
        else:
            # Битва продолжается
            time.sleep(sleep_time)  # Задержка между ходами
