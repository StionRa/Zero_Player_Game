import random

from game.actionlog_model import ActionLog


def attack(attacker, defender, character):
    defender_evasion_chance = defender.dexterity * 0.01
    attacker_evasion_chance = attacker.accuracy * 0.01
    if attacker_evasion_chance < defender_evasion_chance:
        action_description = random.choice(open('game/text/battle/evasion.xml').readlines()).format(
            name=defender.name,
        )
        ActionLog.objects.create(description=action_description, character=character)
        return
    else:
        critical_chance = attacker.luck * 0.01
        defender_evasion_critical_chance = defender.accuracy * 0.01
        damage = 0
        if critical_chance > defender_evasion_critical_chance:
            x_chance = random.randint(1, 2)
            if x_chance == 1:
                damage = attacker.strength * 5 - defender.defense * 0.2
                defender.health -= int(damage)
                attacker.save()
                defender.save()
                action_description = random.choice(
                    open('game/text/battle/battle_character_crit.xml').readlines()).format(
                    name=attacker.name,
                    animal=defender.name,
                    animal_health=defender.health,
                    damage=damage,
                )
                ActionLog.objects.create(description=action_description, character=character)
                return
            elif x_chance == 2:
                damage = attacker.strength * 3 - defender.defense * 0.2
                defender.health -= int(damage)
                attacker.save()
                defender.save()
                action_description = random.choice(
                    open('game/text/battle/battle_character.xml').readlines()).format(
                    name=attacker.name,
                    animal=defender.name,
                    animal_health=defender.health,
                    damage=damage,
                )
                ActionLog.objects.create(description=action_description, character=character)
                return
            else:
                return None
        else:
            damage = attacker.strength * 3 - defender.defense * 0.2
            defender.health -= int(damage)
            attacker.save()
            defender.save()
            action_description = random.choice(
                open('game/text/battle/battle_character.xml').readlines()).format(
                name=attacker.name,
                animal=defender.name,
                animal_health=defender.health,
                damage=damage,
            )
            ActionLog.objects.create(description=action_description, character=character)
