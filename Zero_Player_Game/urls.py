"""
URL configuration for Zero_Player_Game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game.views import index_view, game_info_view, game_index_view, register, user_login, \
    logout_view, game, map_fragment, info_line, news_detail, character_param, view_inventory
from game.create_character_utils import create_character
from faq.views import faq_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Путь к главной странице (index)
    path('', index_view, name='index'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # Путь к странице информации об игре (game_info)
    path('game_info/', game_info_view, name='game_info'),

    # Путь к странице логина
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),

    # Путь к странице регистрации
    path('register/', register, name='register'),
    path('create_character/', create_character, name='create_character'),

    # Путь к странице личного кабинета (game_index)
    path('game_index/', game_index_view, name='game_index'),
    path('game/', game, name='game'),
    path('map_fragment/', map_fragment, name='map_fragment'),
    path('info_line/', info_line, name='info_line'),
    path('character_param/', character_param, name='character_param'),
    path('inventory/', view_inventory, name='inventory'),
    path('faq/', faq_view, name='faq'),
]
