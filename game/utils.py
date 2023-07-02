from game.animal_generator import generate_animals
from game.ai import make_decision_and_move, take_path, move
from game.character_models import Character
from game.animal_model import Animal
from time import sleep
from game.location_model import Location
from game.actionlog_model import ActionLog
from random import choice

def start_game():
    new_animal_generator()


def new_animal_generator():
    generate_animals()


def handle_encounter(character, target_x, target_y):
    animal = Animal.objects.filter(x=target_x, y=target_y).first()
    if animal:
        # Персонаж встретил животное
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
        # Битва между персонажем и животным
        while character.health >= 0 and animal.health >= 0:
            # Персонаж атакует
            character.attack(animal)
            action_description = choice(open('game/text/battle/battle_character.txt').readlines()).format(
                name=character.name,
                species=animal.species,
                animal=animal.name,
                x=target_x,
                y=target_y,
                animal_health=animal.health,
                character_health=character.health
            )
            ActionLog.objects.create(description=action_description, character=character)
            sleep(2)
            # Животное атакует
            animal.attack(character)
            action_description = choice(open('game/text/battle/battle_animal.txt').readlines()).format(
                name=character.name,
                species=animal.species,
                animal=animal.name,
                x=target_x,
                y=target_y,
                animal_health=animal.health,
                character_health=character.health
            )
            ActionLog.objects.create(description=action_description, character=character)
            sleep(2)
            # Проверка условия окончания битвы
            if animal.health <= 0:
                action_description = choice(open('game/text/battle/animal_lose_battle.txt').readlines()).format(
                    name=character.name,
                    species=animal.species,
                    animal=animal.name,
                    x=target_x,
                    y=target_y,
                    animal_health=animal.health,
                    character_health=character.health
                )
                ActionLog.objects.create(description=action_description, character=character)
                # Удаление животного из базы данных
                animal.delete()
            elif character.health <= 0:
                # Персонаж проиграл
                action_description = choice(open('game/text/battle/character_lose_battle.txt').readlines()).format(
                    name=character.name,
                    species=animal.species,
                    animal=animal.name,
                    x=target_x,
                    y=target_y,
                    animal_health=animal.health,
                    character_health=character.health
                )
                ActionLog.objects.create(description=action_description, character=character)
                # Перенос персонажа на координаты (0, 0)
                character.x = 0
                character.y = 0
                character.health = 100
                character.save()
                action_description = f"{character.name} был перенесен в координаты ({character.x}, {character.y})"
                ActionLog.objects.create(description=action_description, character=character)
                # Задержка в 10 минут (время для восстановления)
                sleep(6)

            else:
                # Битва продолжается
                sleep(1)  # Задержка между ходами


def step():
    characters = Character.objects.all()
    for character in characters:
        # Здесь можешь задать целевые координаты для персонажа, например, с помощью случайных значений
        target_x = 1
        target_y = 18
        start_point = make_decision_and_move(character, target_x, target_y)[0]
        target_point = make_decision_and_move(character, target_x, target_y)[1]
        path = take_path(start_point, target_point)
        if path is not None:
            print(path)
            for point in path:
                location = Location.objects.get(x=point[0], y=point[1])
                if location.passable:
                    move(character, point[0], point[1])
                    handle_encounter(character, point[0], point[1])
                    sleep(5)
        else:
            print("Невозможно найти допустимый путь к цели.")
    else:
        print("Недопустимые координаты цели.")
