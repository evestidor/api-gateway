import os

import environ
import sentry_sdk
from sentry_sdk.integrations import django

env = environ.Env()

ENVIRONMENT = env('ENVIRONMENT', default='localhost')

URL_PREFIX = env('URL_PREFIX', default='api')

# PATHS ----------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR_NAME = 'src'

PROJECT_DIR = os.path.join(BASE_DIR, ROOT_DIR_NAME)


# DJANGO SECURITY ------------------------------------------------------------

SECRET_KEY = env('SECRET_KEY', default='SECRET')

DEBUG = env('DEBUG', default=False)

DEFAULT_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=DEFAULT_HOSTS)

DEFAULT_CORS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://0.0.0.0:8000']

CORS_ORIGIN_WHITELIST = env.list('CORS_WHITELIST', default=DEFAULT_CORS)

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True


# DJANGO APPLICATION ---------------------------------------------------------

ROOT_URLCONF = '{}.urls'.format(ROOT_DIR_NAME)

WSGI_APPLICATION = '{}.wsgi.application'.format(ROOT_DIR_NAME)

APPEND_SLASH = True


# DJANGO APPS ----------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = ['rest_framework', 'corsheaders']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS


# DATABASE -------------------------------------------------------------------

DATABASES = {
    # reads os.environ['DATABASE_URL']
    'default': env.db(default='sqlite:///local.db')
}


# TEMPLATES ------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]


# STATIC ---------------------------------------------------------------------

STATIC_URL = '/static/'


# MIDDLEWARES ----------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# I18N & L10N -----------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ERROR REPORTING -------------------------------------------------------------

SENTRY_DSN = env('SENTRY_DSN', default=None)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[django.DjangoIntegration()],
        environment=ENVIRONMENT,
    )


# API GATEWAY ----------------------------------------------------------------

STOCK_MANAGER_URL = env('STOCK_MANAGER_URL', default=None)
