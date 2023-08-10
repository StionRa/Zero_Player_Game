from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from game.character_logic.ai_character_model import AICharacterModel
from game.finder.find_exit_point import find_exit_point
from game.models.town_model import City

input_size = 8
output_size = 2


class Character(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    RACE_CHOICES = (
        ('Human', 'Human'),
        ('Elf', 'Elf'),
        ('Dwarf', 'Dwarf'),
        ('Orc', 'Orc'),
        ('Goblin', 'Goblin'),
        ('Zombie', 'Zombie'),
        ('Skeleton', "Skeleton"),
        ('Centaur', 'Centaur'),
        ('Gryphon', 'Gryphon'),
        ('Nymph', 'Nymph'),
        ('Vampire', 'Vampire'),
        ('Gul', 'Gul'),
        ('Cyborg', 'Cyborg'),
        ('Robot', 'Robot'),
        ('Mutant', 'Mutant'),
        ('Cyborg Elf', 'Cyborg Elf'),
        ('Goblin Geneticist', 'Goblin Geneticist'),
        ('Orc Mechanic', 'Orc Mechanic'),
        ('Humanoids', 'Humanoids'),

        # Add more race choices as needed
    )

    FIRST_PROFESSION = (
        ('Warrior', 'Warrior'),
        ('The Magician', 'The Magician'),
        ('Scout', 'Scout'),
        ('Engineer', 'Engineer'),
        ('Healer', 'Healer'),
        ('Merchant', 'Merchant'),
        ('Artisan', 'Artisan'),
        ('Traveller', 'Traveller'),
        ('Researcher', 'Researcher')

    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    race = models.CharField(max_length=255, choices=RACE_CHOICES)
    profession = models.CharField(max_length=255, choices=FIRST_PROFESSION, default='Warrior')
    health_max = models.IntegerField(default=100)
    mana_max = models.IntegerField(default=100)
    mana = models.IntegerField(default=100)
    stamina_max = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    energy = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    regeneration = models.IntegerField(default=10)
    intuition = models.IntegerField(default=10)
    luck = models.IntegerField(default=10)
    accuracy = models.IntegerField(default=10)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    is_quest_completed = models.BooleanField(default=True)
    have_quest = models.BooleanField(default=False)
    last_regeneration = models.DateTimeField(default=timezone.now)
    last_regeneration_stamina = models.DateTimeField(default=timezone.now)
    pvp_battle = models.IntegerField(default=0)
    mob_battle = models.IntegerField(default=0)
    new_character = models.BooleanField(default=True)

    # flags

    base_experience = 100  # Базовое количество опыта для первого уровня
    level_multiplier = 1.5  # Множитель уровня для экспоненциального повышения опыта
    regeneration_interval = 10

    def check_level_up(self):
        self.required_experience = self.base_experience * (self.level_multiplier ** self.level)
        while self.experience >= self.required_experience:
            self.level += 1
            self.experience = 0
            self.increase_attributes()
            self.required_experience = self.base_experience * (self.level_multiplier ** self.level)
        self.save()

    def increase_attributes(self):
        attribute_increase = self.level * 2  # Define the attribute increase formula as needed
        self.strength += attribute_increase
        self.dexterity += attribute_increase
        self.defense += attribute_increase
        self.intelligence += attribute_increase
        self.energy += attribute_increase
        self.speed += attribute_increase
        self.charisma += attribute_increase
        self.regeneration += attribute_increase
        self.intuition += attribute_increase
        self.luck += attribute_increase
        self.accuracy += attribute_increase

    @classmethod
    def create_ai_model(cls, character_name):
        ai_model = AICharacterModel(input_size=input_size, output_size=output_size)
        file_path = f'{character_name}_ai_model.h5'
        ai_model.save_model_state_to_hdf5(file_path)
        return ai_model

    @classmethod
    def load_model(cls, character_name):
        ai_model = AICharacterModel(input_size=input_size, output_size=output_size)
        file_path = f'{character_name}_ai_model.h5'
        ai_model.load_model_state_from_hdf5(file_path)
        return ai_model

    def regenerate(self):
        if self.health < 0:
            self.health = 0
        elif self.health >= 100:
            self.health = 100
        else:
            if self.health == self.health_max:
                self.health = self.health_max
            else:
                self.health += ((self.health_max - self.health) / self.regeneration) + self.level
        self.save()

    def sleep(self):
        if self.stamina < 0:
            self.stamina = 0
        elif self.stamina >= 100:
            self.stamina = self.stamina_max
        else:
            if self.stamina == self.stamina_max:
                self.stamina = self.stamina_max
            else:
                self.stamina += ((self.stamina_max - self.stamina) / self.regeneration) + self.level

    def is_in_city(self):
        city = City.objects.filter(x_coordinate=self.x, y_coordinate=self.y).first()
        return city is not None

    def leave_city(self):
        # Переместить персонажа из города
        city = City.objects.filter(x_coordinate=self.x, y_coordinate=self.y).first()
        if city:
            exit_point = find_exit_point(city)
            if exit_point:
                self.x, self.y = exit_point
                self.save()
                print(f"Character {self.name} left the city. Coordinates: ({self.x}, {self.y})")
            else:
                print("Exit point from the city not found.")
        else:
            print("Character is not in the city.")
