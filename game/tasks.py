# tasks.py
import logging
from celery import shared_task
from game.character_logic.character_make_decision import make_decision_what_to_do
from game.character_models import Character
from game.animal.animal_generator import generate_animals
import redis
from contextlib import contextmanager

# Create a Redis client to use as a lock
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

CHARACTER_TASK_INTERVAL = 10  # Set the pause time in seconds
LOCK_TTL = 60  # Set the time-to-live for the lock in seconds

# Настройка журнала
logging.basicConfig(filename='celery_tasks.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@contextmanager
def character_lock(character_id):
    character_lock_key = f'character_lock_{character_id}'
    if redis_client.set(character_lock_key, 'locked', ex=LOCK_TTL, nx=True):
        try:
            yield True
        finally:
            redis_client.delete(character_lock_key)
    else:
        yield False


@shared_task  # shared_task - декоратор, который позволяет регистрировать задачи в Celery
def update_character_state():
    logging.info(f"Starting working ...")
    generate_animals()
    logging.info(f"Generate Animals {generate_animals}")
    print(f"Generate Animals {generate_animals}")
    characters = Character.objects.all()
    tasks = []
    for character in characters:
        tasks.append(process_character_utils.delay(character.id))  # delay - метод, который позволяет запускать
        # задачи в Celery
        print(f'Character {character.id} is processing')
        logging.info(f'Character {character.id} is processing')
    logging.info(f"End working ...")
    print(f"End working ...")


@shared_task(max_retries=3)
def process_character_utils(character_id):
    try:
        character = Character.objects.get(id=character_id)
        logging.info(f"Processing character {character_id} - Making decisions...")
        print(f"Processing character {character_id} - Making decisions...")
        make_decision_what_to_do(character)
        logging.info(f"Processing character {character_id} - Decisions completed.")
        print(f"Processing character {character_id} - Decisions completed.")
    except Character.DoesNotExist:
        logging.warning(f"Character with id={character_id} does not exist.")
        print(f"Character with id={character_id} does not exist.")
    except Exception as e:
        logging.error(f"Error in task: {e}")
        print(f"Error in task: {e}")
