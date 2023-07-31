from game.character_logic.another_player import make_choice_what_to_do
from game.models.back_to_city import back_to_city
from game.quest.check_quest_completion import check_quest_completion
from game.quest.quest_logic import make_quest_decision
from game.quest.quest_model import Quest
from game.character_logic.first_action_in_the_world import new_character


def make_decision_what_to_do(character):
    new_character(character)
    character.check_level_up()
    character.regenerate()
    character.sleep()
    check_quest_completion(character)
    make_choice_what_to_do(character)
    active_quests = Quest.objects.filter(character=character, completed=False)
    if not character.is_quest_completed and character.have_quest and active_quests:
        make_quest_decision(character)
    elif character.health <= 0:
        back_to_city(character)
    else:
        back_to_city(character)
