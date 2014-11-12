"""
Django settings for assets_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Keep it secret, keep it safe!
# (Although it's probably irrelevent to this app)
SECRET_KEY = 'a6f@ev$$r^@d4boc-gx^j3l@a=fr4rc^qq3my27zh)pn09$583'

ALLOWED_HOSTS = ['*']

DEBUG = os.environ.get('WSGI_DEBUG', "").lower() == 'true'

INSTALLED_APPS = ['rest_framework']

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = 'assets_server.urls'

WSGI_APPLICATION = 'assets_server.wsgi.application'

LANGUAGE_CODE = 'en-uk'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

REST_FRAMEWORK = {
    # Default format is JSON
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # No complex permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

# Mongo connection
# ===
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

from mappers import TokenManager

DEFAULT_DATABASE = 'assets'
MONGO_URL = os.environ.get(
    'MONGO_URL',
    'mongodb://localhost/{0}'.format(DEFAULT_DATABASE)
)

MONGO = MongoClient(MONGO_URL)

try:
    MONGO_DB = MONGO.get_default_database()
except ConfigurationError:
    MONGO_DB = MONGO[DEFAULT_DATABASE]

TOKEN_MANAGER = TokenManager(data_collection=MONGO_DB["tokens"])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'filename': os.path.join(BASE_DIR, 'django-error.log'),
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 2
        }
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
