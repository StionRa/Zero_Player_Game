from game.models.town_model import City
from game.actionlog_model import ActionLog
from game.quest.quest_generator import QuestGenerator
from random import choice
from game.quest.quest_model import Quest


def enter_city(character):
    print("Entering city...")
    city = City.objects.filter(x_coordinate=character.x, y_coordinate=character.y).first()
    if city:
        print("City found:", city)
        if character.health < character.health_max:
            character.regenerate()
            print("Character health regenerated.")
        if character.health == character.health_max:
            action_description = choice(open('game/text/city/enter_city.txt').readlines()).format(
                name=character.name,
                city=city.name
            )
            ActionLog.objects.create(description=action_description, character=character)
            print("Action log created:", action_description)

            if character.is_quest_completed and not character.have_quest:
                # Если у персонажа нет квестов, выдается новый квест
                new_quest(character)
            elif not character.is_quest_completed and character.have_quest:
                # Если у персонажа есть выполненный квест, вызывается функция completed_quest
                active_quest = Quest.objects.filter(character=character, completed=True).first()
                if active_quest:
                    completed_quest(active_quest, character)
                else:
                    # Если у персонажа есть невыполненный квест, вызывается функция new_quest_target
                    character.have_quest = True
                    character.is_quest_completed = False
                    character.save()
                    character.leave_city()

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
