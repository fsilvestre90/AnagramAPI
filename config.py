# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os

from kombu import Exchange
from kombu import Queue


class BaseConfig(object):
    SECRET_KEY = 'securepassword'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    REDIS_PORT = '6379'
    REDIS_HOST = 'redis'
    REDIS_PASSWORD = 'devpassword'
    REDIS_DB = 0

    RABBIT_HOST = 'rabbit'
    RABBIT_USERNAME = 'guest'
    RABBIT_PASSWORD = 'guest'
    RABBIT_VHOST = '/'
    RABBIT_PORT = '5672'
    BROKER_URL = 'amqp://{0}:{1}@{2}:{3}/{4}'.format(RABBIT_USERNAME, RABBIT_PASSWORD, RABBIT_HOST, RABBIT_PORT,
                                                     RABBIT_VHOST)

    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERY_ACKS_LATE = True

    # Infinite connection retries with Broker if connection lost
    BROKER_CONNECTION_MAX_RETRIES = 0

    CELERY_TASK_RESULT_EXPIRES = 3600 * 24  # 1 day

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERY_CACHE_BACKEND = "memory"

    CELERY_IMPORTS = (
        'app.modules.words.tasks',
    )

    #################################################
    #: Queue and Route related configuration
    #################################################

    CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

    CELERY_QUEUES = (
        Queue('high', Exchange('high'), routing_key='high'),
    )

    CELERY_ROUTES = ({
        'app.modules.words.tasks.save_words': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.prep_task': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.insert_words': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.map_anagrams': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.save_anagrams': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.process_item': {
            'queue': 'high',
            'routing_key': 'high'
        },
        'app.modules.words.tasks.dmap': {
            'queue': 'high',
            'routing_key': 'high'
        },
    }
    )

    DEBUG = False
    ERROR_404_HELP = False

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

    CSRF_ENABLED = False

    ENABLED_MODULES = (
        'words',
        'api',
    )


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
