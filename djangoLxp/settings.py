"""
Paramètres Django du projet DangoLXP

Voir : https://docs.djangoproject.com/en/4.0/topics/settings/

La liste des paramètres possibles : https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env")) # loads the configs from .env

LOGIN_URL='/admin/login/'

ALLOWED_HOSTS = [os.getenv('HOST', 'localhost'),'127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'https://127.0.0.1',]

MIGRATION_MODULES = {'captcha': 'migrations.captcha', 'address': 'migrations.address', 'inscription': 'migrations.inscription'}

# Format des numeros de téléphone avec django-phonenumber-field
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'FR'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
DATE_FORMAT = "d-m-Y"

# Utilise-t-on un stokage sur Oracle)
USE_ORACLE = os.getenv('USE_ORACLE', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# La clé pour avoir accès aux recherchs d'adresses sur google
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
    'django.forms',
    'ajax_datatable',
    'crispy_forms',
    'crispy_bulma',
    'captcha',
    'inscription',
    'django_tables2',
    'formtools',
    'address',
    'storages',
    'leaflet',
    'dal_select2',
    'dal',
    "phonenumber_field",
]

# Pour redéfinir des tempates de widget (avec 'django.forms' dans INSTALLED_APPS
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

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


# Base de donnée
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            #"HOST": os.environ.get("SQL_HOST", "localhost"),
            #"PORT": os.environ.get("SQL_PORT", "5432"),
            #'OPTIONS': {'sslmode': 'False'},
        }
}
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de la cartographie avec Leaflet
LEAFLET_CONFIG = {
# On centre sur la France avec un zoom qui permet de la voir en entier
'DEFAULT_CENTER': (46.36, 1.52),
'DEFAULT_ZOOM': 6,
'MAX_ZOOM':20,
# On utilise un fond de carte dark
'TILES': 'http://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
# TODO : implémenter les clusters de points
'PLUGINS': {
    'markercluster': {
        'css': ['https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.css', 'https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.Default.css'],
        'js': 'https://unpkg.com/leaflet.markercluster/dist/leaflet.markercluster.js',
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

#CRISPY_TEMPLATE_PACK = 'bootstrap4'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bulma"

CRISPY_TEMPLATE_PACK = "bulma"

if USE_ORACLE:
    ORACLE_BUCKET_NAME = os.environ.get('ORACLE_BUCKET_NAME')
    ORACLE_BUCKET_NAMESPACE = os.environ.get('ORACLE_BUCKET_NAMESPACE')
    ORACLE_REGION = os.environ.get('ORACLE_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('ORACLE_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('ORACLE_CUSTOMER_SECRET_KEY')
    AWS_STORAGE_BUCKET_NAME = ORACLE_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = f"{ORACLE_BUCKET_NAMESPACE}.compat.objectstorage.{ORACLE_REGION}.oraclecloud.com"
    AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}"
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    DEFAULT_FILE_STORAGE = 'inscription.utils.MediaStorage'
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{ORACLE_BUCKET_NAME}/media/"
    STATICFILES_STORAGE = 'inscription.utils.StaticStorage'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{ORACLE_BUCKET_NAME}/static/"
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
