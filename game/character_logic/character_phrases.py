from game.actionlog_model import ActionLog
from game.location_model.location_model import Location
from random import choice


def mood_name(mood):
    if 1 <= mood <= 4:
        return "strong_fear"
    elif 5 <= mood <= 8:
        return "fear"
    elif 9 <= mood <= 11:
        return "severe_depression"
    elif 12 <= mood <= 15:
        return "deep_sadness"
    elif 17 <= mood <= 20:
        return "anxiety"
    elif 21 <= mood <= 24:
        return "disappointment"
    elif 25 <= mood <= 28:
        return "discontent"
    elif 29 <= mood <= 32:
        return "anger"
    elif 33 <= mood <= 36:
        return "contempt"
    elif 37 <= mood <= 40:
        return "sadness"
    elif 41 <= mood <= 44:
        return "indifference"
    elif 45 <= mood <= 48:
        return "neutral_state"
    elif 49 <= mood <= 52:
        return "surprise"
    elif 53 <= mood <= 56:
        return "fascination"
    elif 57 <= mood <= 60:
        return "interest"
    elif 61 <= mood <= 64:
        return "relaxation"
    elif 65 <= mood <= 68:
        return "calm"
    elif 69 <= mood <= 72:
        return "confidence"
    elif 73 <= mood <= 76:
        return "pride"
    elif 79 <= mood <= 80:
        return "good_mood"
    elif 81 <= mood <= 84:
        return "joy"
    elif 85 <= mood <= 100:
        return "delight"


def mood_phrases(character):
    stamina = character.stamina
    health = character.health
    mana = character.mana
    energy = character.energy
    charisma = character.charisma
    gender = character.gender

    if gender == 'F':
        mood = (stamina + health + mana + energy + charisma) / 5.2
    elif gender == 'M':
        mood = (stamina + health + mana + energy + charisma) / 5
    else:
        return None

    return int(mood)


def weather_phrases(character):
    cord_x = character.x
    cord_y = character.y
    location = Location.objects.get(x=cord_x, y=cord_y)
    if location.temperature <= 0:
        return


def phrase_choose(character):
    mood = mood_phrases(character)
    name_of_mood = mood_name(mood)
    action_description = choice(open(f'game/text/mood/{name_of_mood}.xml').readlines()).format(
        name=character.name,
    )
    ActionLog.objects.create(description=action_description, character=character)
    return action_description
