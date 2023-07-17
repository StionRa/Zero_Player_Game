from random import choice
from time import sleep

from game.actionlog_model import ActionLog
from game.battle.character_dead import character_dead
from game.quest.check_quest_completion import check_quest_completion


def battle_with_animal(character, animal, quest, target_x, target_y):
    action_description = choice(open('game/text/battle/battle_start.txt').readlines()).format(
        name=character.name,
        species=animal.species,
        animal=animal.name,
        x=target_x,
        y=target_y,
        animal_health=animal.health,
        character_health=character.health
    )
    ActionLog.objects.create(description=action_description, character=character)
    animal.is_active = False
    animal.save()
    sleep(5)
    # Битва между персонажем и животным
    while character.health > 0 and animal.health > 0:
        # Персонаж атакует
        character.attack(animal)
        action_description = choice(
            open('game/text/battle/battle_character.txt').readlines()).format(
            name=character.name,
            species=animal.species,
            animal=animal.name,
            x=target_x,
            y=target_y,
            animal_health=animal.health,
            character_health=character.health
        )
        ActionLog.objects.create(description=action_description, character=character)
        sleep(5)
        # Проверка условия окончания битвы
        if animal.health <= 0:
            action_description_lose = choice(
                open('game/text/battle/animal_lose_battle.txt').readlines()).format(
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
            character.experience += animal.experience
            character.regenerate()
            quest.objective_progress += 1  # Increment the objective progress
            character.save()
            quest.save()
            animal.delete()
            check_quest_completion(character)  # Check if the quest is completed
        # Животное атакует
        sleep(5)
        animal.attack(character)
        action_description = choice(
            open('game/text/battle/battle_animal.txt').readlines()).format(
            name=character.name,
            species=animal.species,
            animal=animal.name,
            x=target_x,
            y=target_y,
            animal_health=animal.health,
            character_health=character.health
        )
        ActionLog.objects.create(description=action_description, character=character)
        sleep(5)
        # Проверка условия окончания битвы
        if character.health <= 0:
            # Персонаж проиграл
            action_description_lose = choice(
                open('game/text/battle/character_lose_battle.txt').readlines()).format(
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
            character_dead(character)
            break
        else:
            # Битва продолжается
            sleep(5)  # Задержка между ходами
