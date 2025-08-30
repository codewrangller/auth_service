from .common import *
import os
import redis

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "0").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ['*']





# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Check if running in Docker
IS_DOCKER = os.environ.get('IS_DOCKER', '').lower() == 'true'

if IS_DOCKER:
    # Docker database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'bill_station'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'PORT': os.environ.get('DB_PORT', '5432')
        }
    }
else:
    # Local database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'bill_station',
            'HOST': 'localhost',
            'USER': os.environ.get('DB_USER_', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD_', 'postgres'),
            'PORT': '5433'
        }
    }



