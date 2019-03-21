import os

import dj_database_url

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
STATIC_ROOT = os.environ.get('STATIC_ROOT', './')
DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL', ''))
