import random
from game.quest.quest_model import Quest


class QuestGenerator:
    QUEST_NAMES = ["Cat Hunt", "Feline Extermination", "Purging the Cat Infestation"]
    QUEST_DESCRIPTIONS = [
        "A quest to find and eliminate animals that have been causing trouble in the kingdom.",
        "The kingdom is overrun with stray cats. Your mission is to hunt them down and eradicate them.",
        "Embark on a cat-hunting adventure and rid the land of these furry pests."
    ]
    QUEST_TASK = ["kill_animal", "kill_animal", "kill_animal"]

    @staticmethod
    def generate_quest(character):
        quest_name = random.choice(QuestGenerator.QUEST_NAMES)
        quest_description = random.choice(QuestGenerator.QUEST_DESCRIPTIONS)
        task_model = random.choice(QuestGenerator.QUEST_TASK)
        experience_reward = random.randint(10, 100)
        objective_quantity = random.randint(1, 50)
        quest = Quest(character=character, name=quest_name, description=quest_description, task_model=task_model,
                      experience_reward=experience_reward, objective_quantity=objective_quantity)
        quest.save()
        return quest
