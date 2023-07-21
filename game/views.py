from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from game.actionlog_model import ActionLog
from game.character_models import Character
from game.inventory.inventory_model import Inventory, InventoryItem
from game.location_model.get_color_temp import get_color_temp
from game.location_model.map_generator import load_map
from game.location_model.print_map import print_map
from game.news.news_model import News, Category
from game.game_options import MIN_TEMPERATURE, MAX_TEMPERATURE
from decimal import Decimal


min_temperature = Decimal(str(MIN_TEMPERATURE))
max_temperature = Decimal(str(MAX_TEMPERATURE))


def index_view(request):
    category = Category.objects.get(name='Game development')
    news = News.objects.filter(category=category)  # Получаем только 3 новости для данной категории
    context = {'category': category, 'news': news}
    return render(request, 'game/index.html', context)


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    context = {'news': news}
    return render(request, 'game/news_detail.html', context)


def game_info_view(request):
    category = Category.objects.get(name='Information')
    news = News.objects.filter(category=category)
    context = {'category': category, 'news': news}
    return render(request, 'game/game_info.html', context)


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
def create_character(request):
    user = request.user
    return render(request, 'game/create_character.html', {'user': user})


@login_required
def game_index_view(request):
    user = request.user
    has_character = Character.objects.filter(user=user).exists()
    if not has_character:
        return redirect('create_character')
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
    map_data, temperature_map, river_map, lake_map = load_map()
    map_html = print_map(map_data, river_map, lake_map, x, y)
    temp = temperature_map[y][x]
    temp_color = get_color_temp(temp)
    temperature_map[y][x] = temp_color
    progress = float((temp - min_temperature) / (max_temperature - min_temperature)) * 100
    conti = {'character': character, "map_data": map_data, 'temperature_map': temperature_map, 'temp': temp,
             'river_map': river_map,
             'lake_map': lake_map, "map_html": map_html, 'temp_color': temp_color,
             "progress": progress}
    return render(request, 'game/map_fragment.html', conti)


@login_required
def info_line(request):
    user = request.user
    character = Character.objects.get(user=user)
    action_logs = ActionLog.objects.filter(character=character).order_by('-timestamp')[:10]
    context = {
        'character': character,
        'action_logs': action_logs
    }
    return render(request, 'game/info_line.html', context)


@login_required
def character_param(request):
    user = request.user
    character = Character.objects.get(user=user)
    context = {
        'character': character
    }
    return render(request, 'game/character_param.html', context)

# views.py


@login_required
def view_inventory(request):
    user = request.user
    character = Character.objects.get(user=user)
    inventory = Inventory.objects.get(character=character)
    inventory_items = InventoryItem.objects.filter(inventory=inventory)

    context = {
        'character': character,
        'inventory_items': inventory_items
    }
    return render(request, 'game/inventory.html', context)

