from django.db import models
from random import choice

from game.actionlog_model import ActionLog
from game.animal.animal_model import Animal
from game.character_models import Character


class AICharacter(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='ai')
    mood = models.CharField(max_length=100, default='neutral')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    is_in_battle = models.BooleanField(default=False)

    def think(self, signal):
        # This is where the signals from the outside come in and are processed.
        if signal == 0.00:
            self.temperature -= 5.00
            self.mood = "cold"
        elif signal == 0.01:
            self.temperature += 35.00
            self.mood = "hot"
        elif signal == 0.02:
            self.is_in_battle = True
            self.mood = 'battle_start'
        elif signal == 0.03:
            self.is_in_battle = False
            self.mood = 'end_battle'
        elif signal == 0.04:
            self.is_in_battle = False
            self.mood = 'end_battle_animal_lose'
        elif signal == 0.05:
            self.is_in_battle = False
            self.mood = 'end_battle_character_lose'
        elif signal == 9.99:
            self.mood = 'new_server_start'

    def talk(self):
        # Логика разговоров на основе текущего настроения
        # В данном примере, просто случайные ответы для иллюстрации

        if self.mood == "cold":
            print(f"{self.character.name}: Brrr, it's cold here.")
        elif self.mood == "hot":
            print(f"{self.character.name}: It's so hot, I need some shade.")
        elif self.mood == "battle_start":
            print(f"{self.character.name}: I'm in the middle of a battle!")
            tart_x = self.character.x
            targ_y = self.character.y
            animal = Animal.objects.filter(x=tart_x, y=targ_y).first()
            action_description = choice(open('game/text/battle/battle_start.xml').readlines()).format(
                name=self.character.name,
                animal=animal.name
            )
            ActionLog.objects.create(description=action_description, character=self.character)
        elif self.mood == 'end_battle_animal_lose':
            tart_x = self.character.x
            targ_y = self.character.y
            animal = Animal.objects.filter(x=tart_x, y=targ_y).first()
            action_description_lose = choice(
                open('game/text/battle/animal_lose_battle.xml').readlines()).format(
                name=self.character.name,
                animal=animal.name
            )
            ActionLog.objects.create(description=action_description_lose, character=self.character)
        elif self.mood == 'end_battle_animal_lose':
            tart_x = self.character.x
            targ_y = self.character.y
            animal = Animal.objects.filter(x=tart_x, y=targ_y).first()
            action_description_lose = choice(
                open('game/text/battle/character_lose_battle.xml').readlines()).format(
                name=self.character.name,
                animal=animal.name
            )
            ActionLog.objects.create(description=action_description_lose, character=self.character)
        elif self.mood == "end_battle":
            print(f"{self.character.name}: End of a battle!")
        elif self.mood == "new_server_start":
            print(f"{self.character.name}: Сколько можно выключать мир? У меня темнеет в глазах и мозг опустошается!!!")
        else:
            print(f"{self.character.name}: Hello, how can I help you?")
