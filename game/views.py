from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .character_models import Character
from .map_generator import generate_map, load_map, check_map_existence
from .print_map import generate_map_html
from .movement_model import move_character


def index_view(request):
    return render(request, 'game/index.html')


def game_info_view(request):
    return render(request, 'game/game_info.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('game_index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'game/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'game/registration.html', {'form': form})


@login_required
def game_index_view(request):
    user = request.user
    has_character = Character.objects.filter(user=user).exists()

    if request.method == 'POST':
        if not has_character:
            return redirect('create_character')
        else:
            move = request.POST.get('move')
            if move in ['w', 'a', 's', 'd']:
                character = Character.objects.get(user=user)
                moved = move_character(character, move)
                if not moved:
                    messages.error(request, 'Invalid move. Try again.')
                    return redirect('game_index')

    if has_character:
        character = Character.objects.get(user=user)
        x = character.x
        y = character.y

        if not check_map_existence():
            generate_map()  # Генерация и сохранение карты, если она не существует

        map_data = load_map()
        map_html = generate_map_html(map_data, x, y)

        return render(request, 'game/game_index.html', {'has_character': has_character, 'character': character, 'map_html': map_html})
    else:
        return render(request, 'game/game_index.html', {'has_character': has_character})



@login_required
def game(request):
    # Проверка авторизации пользователя
    if request.user.is_authenticated:
        return render(request, 'game/game.html')
    else:
        return redirect('login')  # Если пользователь не авторизован, перенаправить на страницу логина
