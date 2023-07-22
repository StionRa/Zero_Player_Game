# faq/views.py

from django.shortcuts import render
from faq.models import GameInfo, FAQTown, FAQItem, FAQItemCategory


def faq_view(request):
    game_info = GameInfo.objects.first()
    cities = FAQTown.objects.all()
    count_cities = len(FAQTown.objects.all())
    items = FAQItem.objects.all()
    items_count = len(FAQItem.objects.all())
    item_category = FAQItemCategory.objects.all()
    return render(request, 'faq/faq.html', {'game_info': game_info, 'cities': cities, "count_cities": count_cities,
                                            'items': items, "items_count": items_count, 'item_category': item_category})
