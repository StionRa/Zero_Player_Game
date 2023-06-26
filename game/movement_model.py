from .map_generator import load_map


def move_character(character, move):
    map_data = load_map()
    x = character.x
    y = character.y

    if move == 'w':
        if map_data[y - 1][x]:
            character.y -= 1
            character.save()
            return True
    elif move == 'a':
        if map_data[y][x - 1]:
            character.x -= 1
            character.save()
            return True
    elif move == 's':
        if map_data[y + 1][x]:
            character.y += 1
            character.save()
            return True
    elif move == 'd':
        if map_data[y][x + 1]:
            character.x += 1
            character.save()
            return True
    return False
