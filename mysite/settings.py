# Django settings for mysite project.
import os, socket


if socket.gethostname() == 'Lees-MacBook-Pro' or socket.gethostname() == 'Brians-MacBook-Air.local':
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('brilee', 'brian.kihoon.lee@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True


PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '' #Defined in local_settings

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL= '/static/'

SECRET_KEY = 'a9ba38f691e2724f5e323e5143da9d73'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
    os.path.join(PROJECT_PATH, 'templates/essays'),
    os.path.join(PROJECT_PATH, 'templates/chemolympiad'),
    os.path.join(PROJECT_PATH, 'templates/homepage'),
    os.path.join(PROJECT_PATH, 'templates/registration'),
    os.path.join(PROJECT_PATH, 'flashcards/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'homepage',
    'chemolympiad',
    'essays',
    'flashcards',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'mydatabase.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

try:
    from local_settings import *
except ImportError:
    pass

