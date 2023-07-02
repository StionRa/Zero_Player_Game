# Zero_Player_Game/celery_1.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения для работы с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zero_Player_Game.settings')

# Создание экземпляра Celery
app = Celery('Zero_Player_Game')

# Настройки рабочих процессов
app.conf.update(
    # Число рабочих процессов (workers), которые будут созданы
    # В данном примере установлено 4 рабочих процесса
    worker_concurrency=1,

    # Дополнительные настройки для ForkPoolWorker
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)
app.conf.broker_connection_retry_on_startup = True

# Загрузка настроек из файла settings.py проекта Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач в файлах tasks.py проекта Django
app.autodiscover_tasks()

