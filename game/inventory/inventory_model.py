from django.db import models
from game.character_models import Character
from game.game_items.item_model import Item


# Модель инвентаря персонажа
class Inventory(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE)

    def create_inventory(self):
        Inventory.objects.create(character=self.character)

    def add_item(self, item, quantity=1):
        existing_item = self.inventoryitem_set.filter(item=item).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            if not self.inventoryitem_set.filter(item=item).exists():
                InventoryItem.objects.create(inventory=self, item=item, quantity=quantity)

    def remove_item(self, item, quantity=1):
        # Проверка, если предмет есть в инвентаре, то уменьшить количество
        existing_item = self.inventoryitem_set.filter(item=item).first()
        if existing_item:
            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                existing_item.delete()
            else:
                existing_item.save()
        else:
            print(f"Item '{item.name}' not found in inventory.")


# Модель предмета в инвентаре
class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
