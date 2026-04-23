import os
import environ
import logging.config

from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = env.bool('DEBUG', True)
BASE_URL = env.str('BASE_URL')

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = env.str('SECRET_KEY', 'django-insecure-3dd^z@cd71x(htv=0$!tfp4)5!rqsb547!=zdcnvwv9bg9k33(')

ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'django_extensions',

    # our-apps
    'accounts.apps.AccountsConfig',
    'career.apps.CareerConfig',
    'quiz.apps.QuizConfig',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Or your chosen static directory

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging

import os
import logging.config

DJANGO_LOG_DIR = env.str(
    "DJANGO_LOG_DIR",
    os.path.join(BASE_DIR, "logs")
)

os.makedirs(DJANGO_LOG_DIR, exist_ok=True)

DJANGO_LOG_FILE = os.path.join(DJANGO_LOG_DIR, "django.log")
DJANGO_ERROR_LOG_FILE = os.path.join(DJANGO_LOG_DIR, "error.log")

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-30s %(levelname)-8s %(message)s"
        },
        "file": {
            "format": "%(asctime)s %(name)-30s %(levelname)-8s %(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": "DEBUG",
        },

        # All logs (DEBUG+), rotated daily
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "level": "DEBUG",
            "filename": DJANGO_LOG_FILE,
            "when": "midnight",
            "interval": 1,
            "backupCount": 14,  # keep 14 days
            "encoding": "utf-8",
        },

        # Errors only, rotated daily
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "level": "ERROR",
            "filename": DJANGO_ERROR_LOG_FILE,
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,  # keep 30 days of errors
            "encoding": "utf-8",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file", "error_file"],
    },
})
