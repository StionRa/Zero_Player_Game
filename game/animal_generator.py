from random import choice
import random
from game.animal_model import Dog, Cat, Animal
from .map_generator import load_map
from game.game_options import MAX_ANIMALS_ON_MAP

GRID_SIZE = 20  # Size of the grid


def calculate_grid_count(map_data):
    passable_count = sum(sum(row) for row in map_data)  # Total number of passable cells
    grid_count = (passable_count // GRID_SIZE)  # Total number of grids
    return grid_count


def generate_animals():
    # Создаем список имен животных
    dog_names = ["Buddy", "Max", "Charlie", "Cooper", "Rocky"]
    cat_names = ["Oliver", "Leo", "Milo", "Simba", "Tiger"]

    # Получаем карту
    map_data = load_map()

    # Вычисляем количество ячеек в сетке
    grid_count = calculate_grid_count(map_data)

    # Проверяем, если количество животных на карте меньше максимального, добавляем новых
    current_animal_count = Animal.objects.count()
    if current_animal_count < MAX_ANIMALS_ON_MAP*grid_count:
        # Генерируем случайное животное
        animal_class = choice([Dog, Cat])

        # Генерируем случайное имя
        if animal_class == Dog:
            name = choice(dog_names)
        else:
            name = choice(cat_names)

        # Создаем экземпляр животного
        animal = animal_class(name=name, age=0, species=animal_class.__name__, health=100,
                              health_max=100, stamina_max=100, stamina=100, strength=random.randint(1, 10),
                              dexterity=random.randint(1, 10), speed=random.randint(1, 10),
                              regeneration=random.randint(1, 10))

        # Получаем доступные координаты для размещения животного
        available_coordinates = []
        for y in range(len(map_data)):
            for x in range(len(map_data[y])):
                if map_data[y][x]:
                    available_coordinates.append((x, y))

        # Вычисляем количество животных, которые должны быть на карте
        animals_to_generate = int(grid_count * MAX_ANIMALS_ON_MAP)

        if animals_to_generate > 0 and len(available_coordinates) > 0:
            for _ in range(animals_to_generate):
                # Проверяем, что есть доступные координаты для размещения животного
                if len(available_coordinates) > 0:
                    # Выбираем случайные координаты из доступных
                    x, y = choice(available_coordinates)

                    # Задаем координаты животного
                    animal.x = x
                    animal.y = y

                    # Удаляем использованные координаты из списка доступных
                    available_coordinates.remove((x, y))

                    # Сохраняем изменения в базе данных
                    animal.save()

        return animal if animal else None
