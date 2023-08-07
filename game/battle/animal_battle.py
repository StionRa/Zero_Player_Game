import time
import torch
from game.animal.animal_inventory import AnimalInventory
from game.battle.character_dead import character_dead
from game.battle.skip_a_turn import skip_turn_and_restore_stamina
from game.quest.check_quest_completion import check_quest_completion
from game.game_options import SLEEP_TIME, CHARACTER_COST_BATTLE_WITH_ANIMAL
from game.battle.atack_standart import attack
from game.character_logic.signal_handler import signal_handler

sleep_time = SLEEP_TIME / 2
cost = CHARACTER_COST_BATTLE_WITH_ANIMAL


def get_or_create_animal_inventory(animal):
    try:
        return animal.animalinventory
    except AnimalInventory.DoesNotExist:
        # If AnimalInventory does not exist, create one
        animal_inventory = AnimalInventory.objects.create(animal=animal)
        return animal_inventory


def battle_with_animal(character, animal, quest, buffer_size=32):
    turn = 0
    signal = 0.02
    signal_handler(character, signal)
    animal_inventory = get_or_create_animal_inventory(animal)
    animal_inventory.generate_loot()
    animal_inventory.save()
    ai_model = character.load_model(character.name)
    # Создание состояния боя для нейронной сети (входной вектор)
    state = [character.health, character.stamina, character.mana, character.defense, animal.health, animal.age,
             animal.defense, animal.strength]
    # Ваша логика для определения флага окончания боя (done)
    # Например, done может быть True, если животное убито, или False, если бой продолжается
    done = animal.health <= 0 or character.health <= 0
    # Битва между персонажем и животным

    # Create an empty buffer to store the samples
    buffer = []

    # Battle loop
    while character.health > 0 and animal.health > 0:
        # Предсказание действия с помощью нейронной сети
        action = ai_model.get_action(state)
        print(f'{turn} - тур боя')
        print(f"{action} - Это выбор модели, что нужно делать")
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
            reward = -1.0  # Штраф за проигрыш
            actions_tensor = torch.tensor([action], dtype=torch.long)
            ai_model.train_batch(buffer, actions_tensor, reward, next_state, done)
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
            reward = 1.0  # Награда за победу
            actions_tensor = torch.tensor([action], dtype=torch.long)
            ai_model.train_batch(buffer, actions_tensor, reward, next_state, done)
            break
        else:
            turn += 1

        # Append the current state and next_state to the buffer
        buffer.append((state, next_state))

        # Check if the buffer has reached the desired size for training
        if len(buffer) >= buffer_size:
            # Prepare the data for training
            batch_states, batch_next_states, batch_actions, batch_rewards = zip(*buffer)
            batch_states = torch.tensor(batch_states, dtype=torch.float).to(ai_model.device)
            batch_next_states = torch.tensor(batch_next_states, dtype=torch.float).to(ai_model.device)
            batch_actions = torch.tensor(batch_actions, dtype=torch.long).unsqueeze(1).to(ai_model.device)
            batch_rewards = torch.tensor(batch_rewards, dtype=torch.float).to(ai_model.device)

            # Train the model using the batch of samples
            ai_model.train_batch(batch_states, batch_actions, batch_rewards, batch_next_states, done)

            # Clear the buffer after training
            buffer = []
