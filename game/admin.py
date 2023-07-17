from django.contrib import admin

from game.location_model.location_model import Location
from game.news.news_model import Category, News, Comment
from game.actionlog_model import ActionLog
from game.animal_model import Animal
from game.character_models import Character
from game.models.town_model import City
from game.quest.quest_model import Quest

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ActionLog)
admin.site.register(Animal)
admin.site.register(Character)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(Quest)
