from .base import *
import os

DEBUG = int({DJANGO_DEBUG})

ALLOWED_HOSTS = ['*']

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{CI_DB_NAME}',
        'USER': '{CI_DB_USER}',
        'PASSWORD': '{CI_DB_PASSWORD}',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }}
}}

INTERNAL_IPS = ['127.0.0.1', ]
