from random import choice
import random
from game.animal.animal_model import Dog, Cat
from game.location_model.map_generator import load_map
from game.location_model.location_model import Location
from django.db import models
from game.animal.animal_model import Animal
from game.models.town_model import City


def calculate_grid_count():
    # Получаем координаты всех городов
    city_coordinates = set((city.x_coordinate, city.y_coordinate) for city in City.objects.all())
    # Получаем координаты всех животных
    animal_coordinates = set((animal.x, animal.y) for animal in Animal.objects.all())
    all_locations = Location.objects.filter(passable=True).values('x', 'y')
    available_coordinates = set((loc['x'], loc['y']) for loc in all_locations) - city_coordinates - animal_coordinates
    return len(available_coordinates)


def count_existing_animals():
    return Animal.objects.count()


generated_animals = []


def generate_animals():
    # Создаем список имен животных
    global generated_animals
    dog_names = ["Buddy", "Max", "Charlie", "Cooper", "Rocky", "Bailey", "Daisy", "Duke", "Bella", "Luna", "Zeus",
                 "Ruby", "Jack", "Molly", "Winston", "Abby", "Toby", "Sadie", "Oscar", "Rosie"]
    cat_names = ["Leo", "Milo", "Simba", "Tiger", "Whiskers", "Chloe", "Jasper", "Willow", "Oliver", "Cleo",
                 "Gizmo", "Nala", "Felix", "Luna", "Muffin", "Simba", "Misty"]

    # Получаем карту
    map_data, _, _, _ = load_map()
    # Вычисляем количество ячеек в сетке
    grid_count = calculate_grid_count()
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
            for y in range(global_min_y, global_max_y + 1):
                for x in range(global_min_x, global_max_x):
                    if map_data[y][x]:
                        available_coordinates.append((x, y))
            # Получаем координаты всех городов
            city_coordinates = set((city.x_coordinate, city.y_coordinate) for city in City.objects.all())

            # Получаем координаты всех животных
            animal_coordinates = set((animal.x, animal.y) for animal in Animal.objects.all())

            # Получаем координаты всех проходимых локаций
            passable_coordinates = set((loc.x, loc.y) for loc in Location.objects.filter(passable=True))

            # Вычисляем свободные координаты как разность множеств проходимых координат и координат городов и животных
            available_coordinates = passable_coordinates - city_coordinates - animal_coordinates
            if animals_to_generate > 0 and len(available_coordinates) > 0:
                generated_animals = []  # Список для хранения сгенерированных животных
                for _ in range(animals_to_generate):
                    # Проверяем, что есть доступные координаты для размещения животного
                    if len(available_coordinates) > 0:
                        # Выбираем случайные координаты из доступных
                        x, y = random.sample(available_coordinates, 1)[0]
                        # Генерируем случайное животное
                        animal_class = choice([Dog, Cat])
                        if animal_class == Dog:
                            name = choice(dog_names)
                        else:
                            name = choice(cat_names)

                        # Создаем экземпляр животного с координатами
                        animal = animal_class(name=name, age=0, species=animal_class.__name__, health=100,
                                              health_max=100, stamina_max=100, stamina=100,
                                              strength=random.randint(3, 6), dexterity=random.randint(3, 6),
                                              defense=random.randint(3, 6), speed=random.randint(3, 6),
                                              regeneration=random.randint(3, 6), intelligence=random.randint(3, 6),
                                              energy=random.randint(3, 6), charisma=random.randint(3, 6),
                                              intuition=random.randint(3, 6), luck=random.randint(3, 6),
                                              accuracy=random.randint(3, 6),
                                              x=x, y=y)

                        generated_animals.append(animal)  # Добавляем сгенерированное животное в список
                        # Удаляем использованные координаты из списка доступных
                        available_coordinates.remove((x, y))
                # Сохраняем все животные в базе данных за один раз
                Animal.objects.bulk_create(generated_animals)
            return generated_animals if generated_animals else None
