from game.battle.pvp_battle import battle_pvp
from game.models.back_to_city import back_to_city
from game.quest.check_quest_completion import check_quest_completion
from game.quest.quest_logic import make_quest_decision
from game.quest.quest_model import Quest


def make_decision_what_to_do(character):
    character.check_level_up()
    character.regenerate()
    check_quest_completion(character)
    battle_pvp(character)
    active_quests = Quest.objects.filter(character=character, completed=False)
    if not character.is_quest_completed and character.have_quest and active_quests:
        make_quest_decision(character)
    elif character.health < character.health_max * 0.3:
        back_to_city(character)
    else:
        back_to_city(character)

