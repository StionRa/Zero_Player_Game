from django.db import models


class MultilingualText(models.Model):
    title = models.TextField(max_length=100)
    text_field_en = models.TextField()
    text_field_uk = models.TextField()
    text_field_ru = models.TextField()
    language_choices = [
        ('en', 'English'),
        ('uk', 'Українська'),
        ('ru', 'Русский'),
        # Добавьте другие языки, если необходимо
    ]
    language = models.CharField(max_length=2, choices=language_choices)

    def get_text_by_language(self):
        if self.language == 'en':
            return self.text_field_en
        elif self.language == 'uk':
            return self.text_field_uk
        elif self.language == 'ru':
            return self.text_field_ru
        else:
            return ''  # Возвращайте пустую строку или что-то другое по умолчанию

    def __str__(self):
        return f"{self.title} - {self.language}: {self.get_text_by_language()}"
