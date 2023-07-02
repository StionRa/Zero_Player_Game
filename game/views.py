from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from game.actionlog_model import ActionLog
from .character_models import Character
from .map_generator import load_map
from .print_map import print_map
from game.tasks import update_character_state
from game.utils import start_game


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
    update_character_state.delay()
    return render(request, 'game/game_index.html',
                  {'has_character': has_character})


@login_required
def game(request):
    # Проверка авторизации пользователя
    if request.user.is_authenticated:
        return render(request, 'game/game.html')
    else:
        return redirect('login')


@login_required
def map_fragment(request):
    user = request.user
    character = Character.objects.get(user=user)
    x = character.x
    y = character.y
    map_data = load_map()
    map_html = print_map(map_data, x, y)
    conti = {'character': character, "map_data": map_data, "map_html": map_html}
    return render(request, 'game/map_fragment.html', conti)


def info_line(request):
    user = request.user
    character = Character.objects.get(user=user)
    start_game()
    action_logs = ActionLog.objects.filter(character=character).order_by('-timestamp')[:10]
    return render(request, 'game/info_line.html', {'action_logs': action_logs})
