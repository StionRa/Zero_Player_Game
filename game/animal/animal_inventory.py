from random import randint

from django.db import models
from game.animal.animal_model import Animal
from game.game_items.item_model import Item


# Модель инвентаря персонажа
class AnimalInventory(models.Model):
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE)

    def create_animal_inventory(self):
        AnimalInventory.objects.create(animal=self.animal)

    def generate_loot(self):
        try:
            item = Item.objects.order_by('?').first()
            quantity = randint(1, 3)
            if item:
                # Добавляем выбранный предмет в инвентарь животного
                self.add_item(item, quantity)
        except AnimalInventory.DoesNotExist:
            self.create_animal_inventory()
            self.generate_loot()

    def add_item(self, item, quantity=1):
        existing_item = self.animalinventoryitem_set.filter(item=item).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            # Проверяем, что предмет не находится в инвентаре животного, чтобы избежать дубликатов
            if not self.animalinventoryitem_set.filter(item=item).exists():
                AnimalInventoryItem.objects.create(animal_inventory=self, item=item, quantity=quantity)

    def remove_item(self, item, quantity=1):
        # Проверка, если предмет есть в инвентаре, то уменьшить количество
        existing_item = self.animalinventoryitem_set.filter(item=item).first()
        if existing_item:
            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                existing_item.delete()
            else:
                existing_item.save()
        else:
            print(f"Item '{item.name}' not found in inventory.")

    def transfer_items_to_character(self, character):
        # Перебираем предметы в инвентаре животного
        for animal_item in self.animalinventoryitem_set.all():
            item = animal_item.item
            quantity = animal_item.quantity

            if not character.inventory:
                character.inventory.create_inventory()
            character.inventory.add_item(item, quantity)
        self.delete()


class AnimalInventoryItem(models.Model):
    animal_inventory = models.ForeignKey(AnimalInventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
