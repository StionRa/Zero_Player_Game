# tasks.py

from celery import shared_task, signals
from game.character_logic.character_make_decision import make_decision_what_to_do
from game.character_models import Character
from game.animal.animal_generator import generate_animals
import redis
import time

# Create a Redis client to use as a lock
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

CHARACTER_TASK_INTERVAL = 10  # Set the pause time in seconds


@shared_task
def update_character_state():
    generate_animals()
    characters = Character.objects.all()
    for character in characters:
        process_character_utils.apply_async(args=(character.id,), task_id=str(character.id))


@shared_task(bind=True)
def process_character_utils(self, character_id):
    character_lock_key = f'character_lock_{character_id}'
    if redis_client.setnx(character_lock_key, 'locked'):
        try:
            generate_animals()
            character = Character.objects.get(id=character_id)
            make_decision_what_to_do(character)
            self.update_state(state='SUCCESS', meta={'message': 'Character actions completed'})
            print("start new circle")
        except Character.DoesNotExist:
            # Character with the given character_id does not exist.
            # You can log a message or take any other appropriate action here.
            print(f"Character with id={character_id} does not exist.")
        finally:
            # Release the lock after completing the task
            redis_client.delete(character_lock_key)


@signals.worker_process_init.connect
def init_worker(**kwargs):
    global character_tasks
    character_tasks = {}


@signals.task_postrun.connect
def task_posturing_handler(task_id, **kwargs):
    character_id = kwargs.get('task_kwargs', {}).get('character_id')
    if character_id:
        time.sleep(CHARACTER_TASK_INTERVAL)  # Pause before getting new task for the character
        character_tasks.pop(character_id, None)
