import time

from game.models.town_model import City
from game.actionlog_model import ActionLog
from game.quest.quest_generator import QuestGenerator
from random import choice
from game.quest.quest_model import Quest
from time import sleep
from game.game_options import SLEEP_TIME

sleep_time = SLEEP_TIME


def enter_city(character):
    print("Entering city...")
    city = City.objects.filter(x_coordinate=character.x, y_coordinate=character.y).first()
    if city:
        if character.health < character.health_max:
            character.regenerate()
            print(f"Character health regenerated. {character.health}/{character.health_max}")
            return
        elif character.health == character.health_max:
            quest = Quest.objects.filter(character=character).first()
            active_quest = Quest.objects.filter(character=character, completed=True).first()
            unfinished_quest = Quest.objects.filter(character=character, completed=False).first()
            if character.is_quest_completed and not character.have_quest and not quest:
                # Если у персонажа нет квестов, выдается новый квест
                new_quest(character)
                return
            elif not character.is_quest_completed and character.have_quest:
                # Если у персонажа есть выполненный квест, вызывается функция completed_quest
                if active_quest:
                    completed_quest(active_quest, character)
                    return
                elif unfinished_quest:
                    # Если у персонажа есть невыполненный квест, вызывается функция leave_city
                    action_description = f"{character.name} goes on an unfinished quest."
                    ActionLog.objects.create(description=action_description, character=character)
                    character.leave_city()
                    return
                else:
                    print("I don`t know what happiness")

            else:
                print("No completed quests found for the character.")

        else:
            print("Character health is not fully regenerated.")
    else:
        print("No city found at the current location.")


def new_quest(character):
    # Generate and assign a new quest to the character
    new_quest_generator = QuestGenerator.generate_quest(character)
    action_description = f"A new quest has been assigned to {character.name}: {new_quest_generator.name}"
    ActionLog.objects.create(description=action_description, character=character)
    character.is_quest_completed = False
    character.have_quest = True
    character.save()
    print("New quest assigned:", new_quest_generator.name)


def completed_quest(quest, character):
    # Reward the character for completing the quest
    character.experience += quest.experience_reward
    action_description = f"{character.name} has completed the quest: {quest.name}"
    ActionLog.objects.create(description=action_description, character=character)
    quest.delete()
    character.is_quest_completed = True
    character.have_quest = False
    character.save()
    print("Quest completed:", quest.name)
