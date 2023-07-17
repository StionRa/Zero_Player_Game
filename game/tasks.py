from celery import shared_task
from game.character_logic.character_make_decision import make_decision_what_to_do
from game.character_models import Character
from game.utils import new_animal_generator


@shared_task
def update_character_state():
    characters = Character.objects.all()
    for character in characters:
        process_character_utils.delay(character.id)


@shared_task
def process_character_utils(character_id):
    character_proc = Character.objects.get(id=character_id)
    make_decision_what_to_do(character_proc)
    new_animal_generator()

