from .common import *
import dj_database_url



SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG', '0').lower() in ['true', 't', '1']
DEBUG = os.environ.get("DEBUG", "0").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True


DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')