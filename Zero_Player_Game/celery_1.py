from __future__ import absolute_import, unicode_literals
# Установка переменной окружения для работы с настройками Django
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zero_Player_Game.settings')


# Создание экземпляра Celery
app = Celery('Zero_Player_Game')

# Загрузка настроек из файла settings.py проекта Django
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_acks_late = True

app.conf.beat_schedule = {
    'run-task-every-1-minute': {
        'task': 'game.tasks.update_character_state',
        'schedule': crontab(minute='*/1'),
    },
}

# Автоматическое обнаружение и регистрация задач в файле tasks.py проекта Django
app.autodiscover_tasks()


