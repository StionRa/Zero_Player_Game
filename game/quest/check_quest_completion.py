from game.quest.quest_model import Quest


def check_quest_completion(character):
    active_quests = Quest.objects.filter(character=character, completed=False)
    if not active_quests:
        return
    else:
        for quest in active_quests:
            if quest.objective_progress >= quest.objective_quantity:
                quest.completed = True  # Mark the quest as completed
                character.is_quest_completed = False
                character.have_quest = True
                quest.save()
                character.save()
