from game.game_options import STAMINA_RESTORATION_AMOUNT


def skip_turn_and_restore_stamina(character):
    # Assuming there is a constant representing the stamina restoration amount
    restoration_value = STAMINA_RESTORATION_AMOUNT * character.level

    # Ensure the restoration value is between 0 and 100
    restoration_value = max(0, min(character.stamina_max, restoration_value))

    # Check if the character is already at full stamina before skipping the turn
    if character.stamina < character.stamina_max:
        # Restore stamina by adding the restoration amount
        character.stamina += restoration_value
        character.save()
