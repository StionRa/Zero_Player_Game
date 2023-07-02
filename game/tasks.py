from celery import shared_task
from time import sleep
from game.utils import step


@shared_task
def update_character_state():
    sleep(5)
    step()

