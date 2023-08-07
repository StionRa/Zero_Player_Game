from game.character_logic.the_master_brain_of_ai import AICharacter
from game.character_models import Character


def signal_handler(character, signal):
    try:
        character = Character.objects.get(name=character.name)
        ai_character = AICharacter.objects.get(character=character)  # Retrieve the associated AICharacter
    except Character.DoesNotExist:
        # Handle the case when the character does not exist
        print(f"Character with name {character.name} does not exist.")
        return
    except AICharacter.DoesNotExist:
        # If AICharacter does not exist, create a new one
        ai_character = AICharacter(character=character)
    ai_character.think(signal)  # Analyze the event and update the AI character's state
    ai_character.save()
    return ai_character.talk()
