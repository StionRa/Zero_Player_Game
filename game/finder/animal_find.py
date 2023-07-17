from game.animal_model import Animal


def find_nearest_animal(character):
    animals = Animal.objects.filter(is_active=True)
    print('get animals from DB')
    if animals:
        nearest_animal = min(animals, key=lambda animal: abs(animal.x - character.x) + abs(animal.y - character.y))
        nearest_x, nearest_y = nearest_animal.x, nearest_animal.y
        print("Nearest animal found at coordinates:", nearest_x, nearest_y)
        return nearest_x, nearest_y
    print("No animals found.")
    return None, None
