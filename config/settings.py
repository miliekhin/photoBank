"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e&4(9-ehb&1j7h5)w7np323e2@w1mh@+ao@f*jbr!d%85&!=sq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'huey.contrib.djhuey',
    'appAuth',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': 'db.sqlite3',
    'immediate': False,
}
SERVER_EMAIL = 'info@photobank.com'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
THUMBS_ROOT = 'thumbs'
THUMBS_URL = '/thumbs/'
MEDIA_PATH = os.path.join(BASE_DIR, MEDIA_ROOT)
THUMBS_PATH = os.path.join(MEDIA_PATH, THUMBS_ROOT)
VIDEO_SLIDESHOW_ROOT = 'video_slideshow'
VIDEO_SLIDESHOW_URL = '/media/video_slideshow/'
VIDEO_SLIDESHOW_PATH = os.path.join(MEDIA_PATH, VIDEO_SLIDESHOW_ROOT)
TEMP_DIR_TOP_PHOTOS_SITE = 'temp_site'
TEMP_DIR_TOP_PHOTOS_USER = 'temp_user'
TOP_PHOTOS_SLIDESHOW_FILE_NAME_SITE = 'top_photos_site.webm'
TOP_PHOTOS_SLIDESHOW_FILE_NAME_USER = 'top_photos_user.webm'
TOP_VIEWED_PHOTOS = 3
ALLOWED_IMAGE_EXT = ['.png', '.jpg', '.jpeg']

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.photos.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

IMAGE_FILE_MAX_SIZE = 5*1024**2
IMAGE_MAX_SIZE_PX = 150
VIDEO_SLIDESHOW_FRAME_DURATION_SEC = 4
