from game.quest.quest_model import Quest


def check_quest_completion(character):
    active_quests = Quest.objects.filter(character=character, completed=False)
    print('check for active quests:', active_quests)
    for quest in active_quests:
        if quest.objective_progress >= quest.objective_quantity:
            quest.completed = True  # Mark the quest as completed
            character.is_quest_completed = True
            character.have_quest = True
            quest.save()
            character.save()
            print(f"Quest completed: {quest.name}")
