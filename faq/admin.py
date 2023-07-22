from django.contrib import admin

from faq.models import GameInfo, FAQTown, FAQItem, FAQItemCategory

admin.site.register(GameInfo)
admin.site.register(FAQTown)
admin.site.register(FAQItem)
admin.site.register(FAQItemCategory)
