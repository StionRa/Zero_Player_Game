from random import choice
import random
from game.animal_model import Dog, Cat
from game.location_model.map_generator import load_map
from game.location_model.location_model import Location
from django.db import models
from game.animal_model import Animal


def calculate_grid_count(map_data):
    passable_count = 0
    for row in map_data:
        for cell in row:
            if cell:
                passable_count += 1
    return passable_count


def count_existing_animals():
    return Animal.objects.count()


generated_animals = []


def generate_animals():
    # Создаем список имен животных
    global generated_animals
    dog_names = ["Buddy", "Max", "Charlie", "Cooper", "Rocky"]
    cat_names = ["Oliver", "Leo", "Milo", "Simba", "Tiger"]

    # Получаем карту
    map_data, _, _, _ = load_map()

    # Вычисляем количество ячеек в сетке
    grid_count = calculate_grid_count(map_data)
    animal_count = int(0.25 * grid_count)
    # Получаем количество уже существующих животных
    existing_animals = count_existing_animals()
    if animal_count > 0:
        # Вычисляем количество животных, которые должны быть на карте
        animals_to_generate = animal_count - existing_animals
        if animals_to_generate > 0:

            # Получаем доступные координаты для размещения животного
            available_coordinates = []
            global_min_x = Location.objects.aggregate(models.Min('x'))['x__min']
            global_max_x = Location.objects.aggregate(models.Max('x'))['x__max']
            global_min_y = Location.objects.aggregate(models.Min('y'))['y__min']
            global_max_y = Location.objects.aggregate(models.Max('y'))['y__max']
            for y in range(global_min_y, global_max_y):
                for x in range(global_min_x, global_max_x):
                    if map_data[y][x]:
                        available_coordinates.append((x, y))

            if animals_to_generate > 0 and len(available_coordinates) > 0:
                generated_animals = []  # Список для хранения сгенерированных животных

                for _ in range(animals_to_generate):
                    # Проверяем, что есть доступные координаты для размещения животного
                    if len(available_coordinates) > 0:
                        # Выбираем случайные координаты из доступных
                        x, y = choice(available_coordinates)

                        # Генерируем случайное животное
                        animal_class = choice([Dog, Cat])
                        if animal_class == Dog:
                            name = choice(dog_names)
                        else:
                            name = choice(cat_names)

                        # Создаем экземпляр животного с координатами
                        animal = animal_class(name=name, age=0, species=animal_class.__name__, health=100,
                                              health_max=100, stamina_max=100, stamina=100,
                                              strength=random.randint(1, 10), dexterity=random.randint(1, 10),
                                              defense=random.randint(1, 10), speed=random.randint(1, 10),
                                              regeneration=random.randint(1, 10),
                                              x=x, y=y)

                        generated_animals.append(animal)  # Добавляем сгенерированное животное в список

                        # Удаляем использованные координаты из списка доступных
                        available_coordinates.remove((x, y))

                # Сохраняем все животные в базе данных за один раз
                Animal.objects.bulk_create(generated_animals)

            return generated_animals if generated_animals else None
