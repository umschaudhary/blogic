from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogic',
        'USER': 'blogicadmin',
        'PASSWORD': 'blogic123',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
    'drf_yasg',
    'django_extensions'
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
SMS_TOKEN = None
