import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2#6%h^=6_%ny6zmq=-(7+9=-=)w1@052p6uj_5yd2^&fx3x2on'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

INSTALLED_APPS += THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.config.urls'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default_formatter': {
            'format': '[%(asctime)s] - [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
logging.config.dictConfig(LOGGING)
