from .map_generator import load_map, add_map_part
import game.game_options as opt

width = opt.WIDTH
height = opt.HEIGHT


def move_character(character, move):
    map_data = load_map()
    x = character.x
    y = character.y

    if move == 'w' and y > 0:
        if map_data[y - 1][x]:
            character.y -= 1
            character.save()
            return True
    elif move == 'w' and y == 0:
        add_map_part(width, height, 'top')
        character.y = 1
        character.save()
        return True
    elif move == 'a' and x > 0:
        if map_data[y][x - 1]:
            character.x -= 1
            character.save()
            return True
    elif move == 'a' and x == 0:
        add_map_part(width, height, 'left')
        character.x = 1
        character.save()
        return True
    elif move == 's' and y < height - 1:
        if map_data[y + 1][x]:
            character.y += 1
            character.save()
            return True
    elif move == 's' and y == height - 1:
        add_map_part(width, height, 'bottom')
        character.y = 1
        character.save()
        return True
    elif move == 'd' and x < width - 1:
        if map_data[y][x + 1]:
            character.x += 1
            character.save()
            return True
    elif move == 'd' and x == width - 1:
        add_map_part(width, height, 'right')
        character.x = 1
        character.save()
        return True

    return False
