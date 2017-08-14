from app.extensions import redis
from celery import group
from celery import subtask

from app import create_celery_app
from app.modules.words.models import AnagramKey, Word
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery = create_celery_app()

ITEMS_PER_BATCH = 100


@celery.task(bind=True)
def save_words(self, data):
    logger.info(self.request.id)
    """
    Insert all the words from the request.
    """
    # clean each word and filter out duplicates
    cleaned_words = list(set([word.strip().lower() for word in data if len(word) > 1]))
    count = 0
    for word in cleaned_words:
        if Word.is_palindrome(word):
            count += 1
        Word.create(word=word, palindrome=Word.is_palindrome(word))
    return None


@celery.task(bind=True)
def map_anagrams(self, result):
    """
    Update all the anagram mappings
    """
    anagram_map = dict()
    for item in Word.all():
        str_hash = ''.join(sorted(item.word))
        if str_hash not in anagram_map:
            anagram_map[str_hash] = set()
            anagram_map[str_hash].add(item.word)
        else:
            words = anagram_map.get(str_hash)
            if item not in words:
                words.add(item.word)
                anagram_map[str_hash] = words

    for anagram_hash, words in anagram_map.items():
        try:
            AnagramKey.load(anagram_hash).delete()
            temp = AnagramKey.create(anagram_hash=anagram_hash)
            temp.words.add(words)
        except KeyError:
            temp = AnagramKey.create(anagram_hash=anagram_hash)
            temp.words.add(words)

# Below is the new approach where I am breaking tasks into sub-parts & querying redis directly
# without Walrus wrapper

# @celery.task(bind=True)
# def prep_task(self, data):
#     cleaned_words = list(set([word.strip().lower() for word in data if len(word) > 1]))
#     return get_batches(cleaned_words, ITEMS_PER_BATCH)
#
# @celery.task(bind=True)
# def insert_words(self, cleaned_words):
#     with redis.pipeline() as pipe:
#         pipe.multi()
#
#         for word in cleaned_words:
#             pipe.hset("words", word, Word.is_palindrome(word))
#         pipe.execute()

# @celery.task(bind=True)
# def map_anagrams(self):
#     anagram_map = dict()
#     for item in Word.all():
#         str_hash = ''.join(sorted(item.word))
#         if str_hash not in anagram_map:
#             anagram_map[str_hash] = set()
#             anagram_map[str_hash].add(item.word)
#         else:
#             words = anagram_map.get(str_hash)
#             if item not in words:
#                 words.add(item.word)
#                 anagram_map[str_hash] = words
#     return anagram_map


# @celery.task(bind=True)
# def save_anagrams(self, anagram_map):
#     with redis.pipeline() as pipe:
#         pipe.multi()
#
#         for anagram_hash, words in anagram_map.items():
#             try:
#                 AnagramKey.load(anagram_hash).delete()
#                 temp = AnagramKey.create(anagram_hash=anagram_hash)
#                 temp.words.add(words)
#             except KeyError:
#                 temp = AnagramKey.create(anagram_hash=anagram_hash)
#                 temp.words.add(words)
#             pipe.hset("anagrams", word, Word.is_palindrome(word))
#         pipe.execute()
#
#
#
# @celery.task(bind=True)
# def process_item(self, obj_list):
#     insert_words.s(obj_list).delay()
#
# @celery.task()
# def dmap(it, callback):
#     # Map a callback over an iterator and return as a group
#     callback = subtask(callback)
#     return group(callback.clone([arg, ]) for arg in it)()
#
#
# def get_batches(work, batch_size):
#     batches = []
#
#     while work:
#         t_batch_size = min(len(work), batch_size)
#
#         batches.append(work[:t_batch_size])
#         work = work[t_batch_size:]
#
#     return batches
