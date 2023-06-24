import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .character_models import Character


@login_required
def create_character(request):
    user = request.user
    # Check if the user already has a character
    if Character.objects.filter(user=user).exists():
        return redirect('game_index')
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        race = request.POST['race']

        # Создание экземпляра персонажа
        character = Character.objects.create(user=request.user,
                                             name=name,
                                             gender=gender,
                                             race=race,
                                             health_max=100,
                                             mana_max=20,
                                             mana=20,
                                             stamina_max=100,
                                             stamina=100,
                                             health=100,
                                             strength=random.randint(1, 10),
                                             dexterity=random.randint(1, 10),
                                             intelligence=random.randint(1, 10),
                                             energy=random.randint(1, 10),
                                             speed=random.randint(1, 10),
                                             charisma=random.randint(1, 10),
                                             regeneration=random.randint(1, 10),
                                             intuition=random.randint(1, 10),
                                             luck=random.randint(1, 10),
                                             accuracy=random.randint(1, 10))

        character.save()

        return redirect('game_index')  # Перенаправление на страницу кабинета пользователя

    return render(request, 'game/create_character.html')
