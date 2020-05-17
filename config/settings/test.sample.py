from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ci',
        'USER': 'runner',
        'PASSWORD': '',
        'HOST': 'postgres',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}
SMS_TOKEN = None
