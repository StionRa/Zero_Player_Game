"""
animal_battle.py

This module contains functions related to character battles with animals.

Functions:
    new_buffer: Append battle data to the buffer.
    get_or_create_animal_inventory: Get or create an AnimalInventory for the given animal.
    train_model: Train the AI model using the battle data buffer.
    battle_with_animal: Perform a battle between a character and an animal.

Usage example:
    battle_with_animal(character, animal, quest)
"""

import time
import logging
from game.animal.animal_inventory import AnimalInventory
from game.battle.character_dead import character_dead
from game.battle.skip_a_turn import skip_turn_and_restore_stamina
from game.quest.check_quest_completion import check_quest_completion
from game.game_options import SLEEP_TIME, CHARACTER_COST_BATTLE_WITH_ANIMAL
from game.battle.atack_standart import attack
from game.character_logic.signal_handler import signal_handler

# Configure the logger
logging.basicConfig(filename='battle_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# The time to wait between actions
sleep_time = SLEEP_TIME / 2
# The cost of a battle with an animal
cost = CHARACTER_COST_BATTLE_WITH_ANIMAL


def new_buffer(buffer, state, next_state, action, reward):
    """
        Append battle data to the buffer.

        Args:
            buffer (list): The buffer to store battle data.
            state (list): The current state.
            next_state (list): The next state.
            action (int): The action taken.
            reward (float): The reward received.

        Returns:
            list: The updated buffer.
    """
    buffer.append((state, next_state, action, reward))
    return buffer


def get_or_create_animal_inventory(animal):
    """
    Get or create an AnimalInventory for the given animal.

    Args:
        animal (Animal): The animal instance.

    Returns:
        AnimalInventory: The animal's inventory.
    """
    try:
        return animal.animalinventory
    except AnimalInventory.DoesNotExist:
        try:
            # If AnimalInventory does not exist, create one
            animal_inventory = AnimalInventory.objects.create(animal=animal)
            return animal_inventory
        except Exception as e:
            print(f"Error creating animal inventory: {e}")
            # Handle the error as needed, e.g., raise an exception or log it
            # Return None or a default value if the inventory creation fails
            return None


def train_model(buffer, ai_model, character, done):
    """
        Train the AI model using the battle data buffer.

        Args:
            buffer (list): The buffer containing battle data.
            ai_model (AICharacterModel): The AI model instance.
            character (Character): The character instance.
            done (bool): Flag indicating if the battle is done.
    """
    if not buffer:
        return

    states, next_states, actions, rewards = zip(*buffer)
    batch = list(zip(states, next_states, actions, rewards))

    ai_model.train_batch(batch, done, character)


def battle_with_animal(character, animal, quest):
    """
        Perform a battle between a character and an animal.

        Args:
            character (Character): The character instance.
            animal (Animal): The animal instance.
            quest (Quest): The quest instance.
    """
    turn = 0
    signal = 0.02
    signal_handler(character, signal)
    animal_inventory = get_or_create_animal_inventory(animal)
    animal_inventory.generate_loot()
    animal_inventory.save()
    ai_model = character.load_model(character.name)
    buffer = []

    # Log the start of the battle
    logging.info(f"Battle started between {character.name} and {animal.name} at {time.ctime()}")
    print(f"Battle started between {character.name} and {animal.name} at {time.ctime()}")

    # Battle loop
    while character.health > 0 and animal.health > 0:
        state = [character.health, character.stamina, character.mana, character.defense, animal.health, animal.age,
                 animal.defense, animal.strength]
        # Предсказание действия с помощью нейронной сети
        action = ai_model.get_action(state)
        if action == 0:
            attack(character, animal, character)
        elif action == 1:
            skip_turn_and_restore_stamina(character)
        time.sleep(sleep_time)
        # Получение следующего состояния и флага окончания боя
        next_state = [character.health, character.stamina, character.mana, character.defense,
                      animal.health, animal.age, animal.defense, animal.strength]
        # Животное атакует
        if animal.health > 0:
            attack(animal, character, character)
            time.sleep(sleep_time)
        # Проверка условия окончания битвы
        done = animal.health <= 0 or character.health <= 0
        if character.health <= 0:
            # Персонаж проиграл
            signal = 0.05
            signal_handler(character, signal)
            # Перенос персонажа в ближайший город
            animal.is_active = True
            animal.quest_character = None
            animal.save()
            character.stamina = max(character.stamina - cost, 0)
            character_dead(character)
            reward = -1.0  # Награда за продолжение боя
            buffer = new_buffer(buffer, state, next_state, action, reward)
            train_model(buffer, ai_model, character, done)
            logging.info(f"Battle ended between {character.name} and {animal.name} at {time.ctime()} - animal won")
            print(f"Battle ended between {character.name} and {animal.name} at {time.ctime()} - animal won")
            break
        elif animal.health <= 0:
            signal = 0.04
            signal_handler(character, signal)
            # Удаление животного из базы данных
            if animal.animalinventory:
                animal.animalinventory.transfer_items_to_character(character)
            character.experience += animal.experience
            character.mob_battle += 1
            quest.objective_progress += 1  # Increment the objective progress
            character.stamina = max(character.stamina - cost, 0)
            character.save()
            quest.save()
            animal.is_active = False
            animal.save()
            animal.delete()
            check_quest_completion(character)  # Check if the quest is completed
            reward = 1.0  # Награда за продолжение боя
            buffer = new_buffer(buffer, state, next_state, action, reward)
            train_model(buffer, ai_model, character, done)
            logging.info(f"Battle ended between {character.name} and {animal.name} at {time.ctime()} - character won")
            print(f"Battle ended between {character.name} and {animal.name} at {time.ctime()} - character won")
            break
        else:
            turn += 1
            reward = 0.0  # Награда за продолжение боя
            buffer = new_buffer(buffer, state, next_state, action,  reward)
            logging.info(f"Turn {turn} - Action: {action} - State: {state} - Next State: {next_state}")
            print(f"Turn {turn} - Action: {action} - State: {state} - Next State: {next_state}")
