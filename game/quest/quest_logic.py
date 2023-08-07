from game.animal.animal_model import Animal
from game.battle.animal_battle import battle_with_animal
from game.finder.animal_find import find_nearest_animal
from game.models.back_to_city import back_to_city
from game.movement.repeat_move_to_target import repeat_move
from game.quest.quest_model import Quest
from game.utils import handle_no_active_animal_error


def make_quest_decision(character):
    active_quests = Quest.objects.filter(character=character, completed=False)
    have_quest = character.have_quest
    complited_quest = character.is_quest_completed
    print(f"Making quest decision for character: {character.name}")
    if not complited_quest and have_quest:
        for quest in active_quests:
            if quest.task_model == "kill_animal":
                print('look for nearest animal')
                target_x, target_y = find_nearest_animal(character)
                if target_x is None or target_y is None:
                    handle_quest_error(character, quest)
                else:
                    nearest_animal = Animal.objects.filter(x=target_x, y=target_y).first()
                    nearest_animal.is_active = False
                    nearest_animal.quest_character = character
                    nearest_animal.save()
                    repeat_move(character, target_x, target_y)
                    print(f'repeat move to target: {target_x}, {target_y}')
                    if nearest_animal:
                        if quest.objective_progress < quest.objective_quantity:
                            if nearest_animal is None:
                                # No animal found at the specified location
                                continue
                            else:
                                battle_with_animal(character, nearest_animal, quest)
                    else:
                        handle_no_active_animal_error(character, quest)
                        continue
            elif quest.task_model == 'goto_city':
                back_to_city(character)
            else:
                handle_quest_error(character, quest)
                print('error')
    elif not have_quest and complited_quest:
        back_to_city(character)

    else:
        back_to_city(character)


def handle_quest_error(character, quest):
    # Handle the error for the specific quest
    print(f"Error occurred for quest: {quest.name} by character: {character.name}")
    # You can perform additional actions or logging here


def handle_no_quest_error(character):
    # Handle the error when there are no active quests
    print(f"No active quests found for character: {character.name}")
    # You can perform additional actions or logging here
    # For example, you can assign a default quest to the character or take other actions
