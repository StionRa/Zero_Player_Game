from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .character_models import Character
from .inventory.inventory_model import Inventory

strength = 0
dexterity = 0
defense = 0
intelligence = 0
energy = 0
speed = 0
charisma = 0
regeneration = 0
intuition = 0
luck = 0
accuracy = 0


@login_required
def create_character(request):
    global strength, dexterity, defense, intelligence, energy, speed, charisma, regeneration, intuition, luck, accuracy
    user = request.user
    # Check if the user already has a character
    if Character.objects.filter(user=user).exists():
        return redirect('game_index')
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        race = request.POST['race']
        profession = request.POST['profession']

        if race == 'Human':
            strength += 8
            dexterity += 9
            defense += 8
            intelligence += 6
            energy += 8
            speed += 7
            charisma += 6
            regeneration += 4
            intuition += 5
            luck += 7
            accuracy += 4

        elif race == 'Elf':
            strength += 9
            dexterity += 7
            defense += 5
            intelligence += 10
            energy += 9
            speed += 10
            charisma += 8
            regeneration += 6
            intuition += 4
            luck += 8
            accuracy += 8

        elif race == 'Dwarf':
            strength += 10
            dexterity += 5
            defense += 10
            intelligence += 5
            energy += 7
            speed += 4
            charisma += 4
            regeneration += 5
            intuition += 6
            luck += 6
            accuracy += 5

        elif race == 'Orc':
            strength += 10
            dexterity += 8
            defense += 9
            intelligence += 5
            energy += 10
            speed += 4
            charisma += 4
            regeneration += 10
            intuition += 3
            luck += 6
            accuracy += 4

        elif race == 'Goblin':
            strength += 5
            dexterity += 6
            defense += 5
            intelligence += 9
            energy += 6
            speed += 10
            charisma += 6
            regeneration += 12
            intuition += 7
            luck += 9
            accuracy += 8

        elif race == 'Zombie':
            strength += 8
            dexterity += 4
            defense += 12
            intelligence += 3
            energy += 2
            speed += 2
            charisma += 1
            regeneration += 15
            intuition += 1
            luck += 2
            accuracy += 1

        elif race == 'Skeleton':
            strength += 6
            dexterity += 7
            defense += 8
            intelligence += 6
            energy += 5
            speed += 7
            charisma += 3
            regeneration += 5
            intuition += 5
            luck += 5
            accuracy += 6

        elif race == 'Centaur':
            strength += 9
            dexterity += 8
            defense += 7
            intelligence += 5
            energy += 7
            speed += 9
            charisma += 6
            regeneration += 7
            intuition += 7
            luck += 5
            accuracy += 7

        elif race == 'Gryphon':
            strength += 10
            dexterity += 9
            defense += 8
            intelligence += 6
            energy += 8
            speed += 10
            charisma += 6
            regeneration += 6
            intuition += 6
            luck += 8
            accuracy += 10

        elif race == 'Nymph':
            strength += 5
            dexterity += 6
            defense += 4
            intelligence += 10
            energy += 10
            speed += 8
            charisma += 9
            regeneration += 8
            intuition += 9
            luck += 9
            accuracy += 9

        elif race == 'Vampire':
            strength += 8
            dexterity += 8
            defense += 6
            intelligence += 9
            energy += 10
            speed += 9
            charisma += 7
            regeneration += 12
            intuition += 7
            luck += 8
            accuracy += 8

        elif race == 'Gul':
            strength += 5
            dexterity += 4
            defense += 3
            intelligence += 12
            energy += 12
            speed += 3
            charisma += 2
            regeneration += 15
            intuition += 10
            luck += 9
            accuracy += 12

        elif race == 'Cyborg':
            strength += 10
            dexterity += 10
            defense += 10
            intelligence += 10
            energy += 10
            speed += 10
            charisma += 10
            regeneration += 10
            intuition += 10
            luck += 10
            accuracy += 10

        elif race == 'Robot':
            strength += 12
            dexterity += 5
            defense += 15
            intelligence += 15
            energy += 15
            speed += 5
            charisma += 1
            regeneration += 0
            intuition += 3
            luck += 0
            accuracy += 15

        elif race == 'Mutant':
            strength += 8
            dexterity += 7
            defense += 6
            intelligence += 8
            energy += 8
            speed += 8
            charisma += 5
            regeneration += 10
            intuition += 6
            luck += 5
            accuracy += 7

        elif race == 'Cyborg Elf':
            strength += 9
            dexterity += 9
            defense += 7
            intelligence += 11
            energy += 9
            speed += 9
            charisma += 7
            regeneration += 6
            intuition += 8
            luck += 9
            accuracy += 9

        elif race == 'Goblin Geneticist':
            strength += 6
            dexterity += 7
            defense += 4
            intelligence += 12
            energy += 12
            speed += 6
            charisma += 4
            regeneration += 12
            intuition += 10
            luck += 9
            accuracy += 10

        elif race == 'Orc Mechanic':
            strength += 11
            dexterity += 6
            defense += 10
            intelligence += 6
            energy += 8
            speed += 5
            charisma += 5
            regeneration += 7
            intuition += 5
            luck += 6
            accuracy += 6

        elif race == 'Humanoids':
            strength += 7
            dexterity += 7
            defense += 7
            intelligence += 7
            energy += 7
            speed += 7
            charisma += 7
            regeneration += 7
            intuition += 7
            luck += 7
            accuracy += 7

        if profession == 'Warrior':
            strength += 10
            dexterity += 8
            defense += 9
            intelligence += 6
            energy += 8
            speed += 7
            charisma += 6
            regeneration += 5
            intuition += 6
            luck += 7
            accuracy += 6

        elif profession == 'The Magician':
            strength += 6
            dexterity += 7
            defense += 6
            intelligence += 10
            energy += 12
            speed += 6
            charisma += 8
            regeneration += 10
            intuition += 10
            luck += 8
            accuracy += 8

        elif profession == 'Scout':
            strength += 7
            dexterity += 10
            defense += 6
            intelligence += 8
            energy += 8
            speed += 10
            charisma += 7
            regeneration += 7
            intuition += 9
            luck += 9
            accuracy += 10

        elif profession == 'Engineer':
            strength += 7
            dexterity += 9
            defense += 7
            intelligence += 11
            energy += 9
            speed += 8
            charisma += 6
            regeneration += 6
            intuition += 8
            luck += 7
            accuracy += 7

        elif profession == 'Healer':
            strength += 6
            dexterity += 6
            defense += 7
            intelligence += 9
            energy += 10
            speed += 7
            charisma += 9
            regeneration += 12
            intuition += 10
            luck += 9
            accuracy += 7

        elif profession == 'Merchant':
            strength += 5
            dexterity += 8
            defense += 5
            intelligence += 10
            energy += 10
            speed += 6
            charisma += 12
            regeneration += 6
            intuition += 10
            luck += 10
            accuracy += 5

        elif profession == 'Artisan':
            strength += 6
            dexterity += 9
            defense += 6
            intelligence += 8
            energy += 9
            speed += 6
            charisma += 8
            regeneration += 8
            intuition += 7
            luck += 7
            accuracy += 6

        elif profession == 'Traveller':
            strength += 7
            dexterity += 7
            defense += 8
            intelligence += 7
            energy += 8
            speed += 9
            charisma += 9
            regeneration += 8
            intuition += 8
            luck += 9
            accuracy += 8

        elif profession == 'Researcher':
            strength += 5
            dexterity += 6
            defense += 5
            intelligence += 12
            energy += 10
            speed += 6
            charisma += 6
            regeneration += 7
            intuition += 11
            luck += 8
            accuracy += 7

        # Создание экземпляра персонажа
        character = Character.objects.create(user=request.user,
                                             name=name,
                                             gender=gender,
                                             race=race,
                                             profession=profession,
                                             health_max=100,
                                             mana_max=20,
                                             mana=20,
                                             stamina_max=100,
                                             stamina=100,
                                             health=100,
                                             strength=strength,
                                             dexterity=dexterity,
                                             defense=defense,
                                             intelligence=intelligence,
                                             energy=energy,
                                             speed=speed,
                                             charisma=charisma,
                                             regeneration=regeneration,
                                             intuition=intuition,
                                             luck=luck,
                                             accuracy=accuracy,
                                             )
        character.create_ai_model(character.name)
        get_or_create_inventory(character)
        character.save()

        return redirect('game_index')  # Перенаправление на страницу кабинета пользователя

    return render(request, 'game/create_character.html')


def get_or_create_inventory(character):
    try:
        return character.inventory.create_inventory()
    except Inventory.DoesNotExist:
        # If AnimalInventory does not exist, create one
        character_inventory = Inventory.objects.create(character=character)
        return character_inventory
