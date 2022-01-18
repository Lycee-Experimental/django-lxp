"""
Paramètres Django du projet DangoLXP

Voir : https://docs.djangoproject.com/en/4.0/topics/settings/

La liste des paramètres possibles : https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL='/admin/login/'

ALLOWED_HOSTS = ['davy39.pythonanywhere.com', '127.0.0.1', 'https://lxp-app.herokuapp.com', 'inscription.cf']
CSRF_TRUSTED_ORIGINS = ['https://inscription.cf','http://lxp-app.herokuapp.com','http://127.0.0.1','https://lxp-app.herokuapp.com','https://127.0.0.1',]

MIGRATION_MODULES = {'captcha': 'migrations.captcha', 'address': 'migrations.address', 'inscription': 'migrations.inscription'}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
DATE_FORMAT = "d-m-Y"

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env")) # loads the configs from .env
USE_S3 = os.getenv('USE_S3', False)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))

# Applications utilisées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_countries',
    'captcha',
    'inscription',
    'django_tables2',
    'formtools',
    'address',
    'storages',
    'leaflet',
    'dal_select2',
    'dal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'djangoLxp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'djangoLxp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

LEAFLET_CONFIG = {
    # Configuration de la cartographie
# On centre sur la France avec un zoom qui permet de la voir en entier
'DEFAULT_CENTER': (46.36, 1.52),
'DEFAULT_ZOOM': 6,
# On utilise un fond de carte dark
'TILES': 'http://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
# TODO : implémenter les clusters de points
'PLUGINS': {
    'markercluster': {
        'css': ['https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css'],
        'js': 'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js',
        'auto-include': True,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if USE_S3:
# Si stockage des fichiers statiques et média sur AWS S3
    # Les codes secrets sont dans les variables d'environnement
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'django-lxp'
    # Important, sinon access denied, et il faut activer l'ACL dans les propriétés des permissions du buket
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {     'CacheControl': 'max-age=86400', }
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'inscription.utils.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'inscription.utils.MediaStorage'  # <-- here is where we reference it
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

import django_heroku

# Attention : s'il n'y a pas staticfiles=False le dossier par défaut static_root ou AWS n'est pas utilisé
django_heroku.settings(locals(), staticfiles=False)