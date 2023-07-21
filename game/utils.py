from game.animal.animal_generator import generate_animals


def new_animal_generator():
    generate_animals()


def handle_no_active_animal_error(character, quest):
    print(f"Sorry {character}. No active animals for the {quest} found at the target location.")
    # Perform any necessary actions or error handling specific to the quest or character
    # For example, you can mark the quest as failed or handle it based on your game logic.
