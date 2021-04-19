"""
Django settings for URLShortener project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("URL_SHORTENER_SK", "adhg5UYG6FGGJSGEFS%^$SDF")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# TODO: fill following list in the deployment step
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Django built-in apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External apps:
    'rest_framework',
    # 'oauth2_provider',
    'corsheaders',  # handling CORS
    'django_extensions',  # tools

    # Internal apps:
    "apps.core",
    "apps.shortener",
    "apps.redirect"
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'URLShortener.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'URLShortener.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30
}

CELERY_BROKER_URL = os.getenv('URL_SHORTENER_CELERY_BROKER_URL',
                              'amqp://url_shortener:url_shortener@localhost:5672/url_shortener_vhost')
CELERY_RESULT_BACKEND = os.getenv('URL_SHORTENER_CELERY_RESULT_BACKEND', 'redis://localhost')

CORS_ORIGIN_WHITELIST = (
    'http://google.com',  # example
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'content-disposition',
    'cache-control',
    'pragma',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("URL_SHORTENER_PG_NAME", "postgres"),
        'USER': os.getenv("URL_SHORTENER_PG_USER", "postgres"),
        'HOST': os.getenv("URL_SHORTENER_PG_HOST", "localhost"),
        'PASSWORD': os.getenv("URL_SHORTENER_PG_PASSWORD", "postgres"),
        'PORT': os.getenv("URL_SHORTENER_PG_PORT", 5432)
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# The path of the django output log file.
URL_SHORTENER_DJANGO_LOG = os.path.join(
    os.getenv("URL_SHORTENER_DJANGO_LOG", BASE_DIR), "url_shortener.log"
)
if not os.path.isdir(os.path.dirname(URL_SHORTENER_DJANGO_LOG)):
    os.makedirs(os.path.dirname(URL_SHORTENER_DJANGO_LOG))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': os.getenv('URL_SHORTENER_FILE_LOG_LVL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': URL_SHORTENER_DJANGO_LOG,
            'formatter': 'standard',
        }
    },
    'root': {
        'handlers': ['file'],
        'level': os.getenv('URL_SHORTENER_ROOT_LOG_LVL', 'INFO'),
    },
}

STATIC_URL = os.getenv('URL_SHORTENER_STATIC_URL', 'static/')
STATIC_ROOT = os.getenv('URL_SHORTENER_STATIC_ROOT', os.path.join(BASE_DIR, STATIC_URL))

MEDIA_URL = os.getenv('URL_SHORTENER_MEDIA_URL', 'media/')
MEDIA_ROOT = os.getenv('URL_SHORTENER_MEDIA_ROOT', os.path.join(BASE_DIR, MEDIA_URL))
if not os.path.isdir(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHORTENER_MIN_HASH_LENGTH = 5

APPEND_SLASH = True
