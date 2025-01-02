"""
Django settings for dart project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from celery.schedules import crontab
import ecs_logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w0)lou!3#nnf=1o!s#)pe)(g0p$3h)+1b+c1fsmt_a5-q03gb_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get("SERVER_MODE") == "production" else True

ALLOWED_HOSTS = ['localhost','dart-admin.duckdns.org']
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    'https://dart-admin.duckdns.org',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corp_sync',
    'django_celery_results',  # 결과 저장을 위해
    'django_celery_beat',     # 주기적 작업 관리
    'import_export',
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

ROOT_URLCONF = 'dart.urls'

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

WSGI_APPLICATION = 'dart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 정적 파일 URL 경로 (기본값)
STATIC_URL = 'static/'

# 정적 파일을 수집할 디렉터리 (배포용)
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# settings.py

# Celery 설정
CELERY_BROKER_URL = os.environ.get("REDIS_URL")  # Redis를 브로커로 사용 (localhost:6379에 Redis가 실행 중)
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")  # Redis를 결과 백엔드로 사용
CELERY_ACCEPT_CONTENT = ['json']  # JSON 포맷을 사용하여 직렬화
CELERY_TASK_SERIALIZER = 'json'  # 작업 직렬화 포맷 설정
CELERY_RESULT_SERIALIZER = 'json'  # 작업 직렬화 포맷 설정
# settings.py 또는 Celery 설정 파일에서
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
print("celery conf")
print(CELERY_BROKER_URL)
print(CELERY_RESULT_BACKEND)

# # Celery 설정 (기간 설정이 필요한 경우, 주기적인 작업에 대한 설정)
# CELERY_BEAT_SCHEDULE = {
#     'api-call-task': {
#         'task': 'company.tasks.enqueue_pending_codes',  # 작업을 실행할 함수 경로
#         'schedule': crontab(minute=0, hour=18),  # 매일 18시에 작업 실행
#     },
# }

# Celery result 저장 설정
CELERY_RESULT_EXPIRES = 3600  # 결과 저장 시간 (초 단위)
CELERY_TIMEZONE = 'Asia/Seoul'  # 시간대 설정 (예: 서울 기준)

# Celery 작업 결과 제한 설정
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # 작업 시간 제한 (초 단위)

# # Celery 시리얼라이저 설정
# CELERY_TASK_QUEUES = {
#     'default': {
#         'exchange': 'default',
#         'binding_key': 'default',
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "INFO",
        "handlers": ["root","console"],
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s %(module)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%Y/%d/%b %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
        "ecsprint": {
            "()": ecs_logging.StdlibFormatter,
        },
    },
    "handlers": {
        "root": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/log.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 2,
            "backupCount": 5,
        },
        "ecs": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "ecsprint",
        },
        "celery": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/celery.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 2,
            "backupCount": 2,
        },
        "django": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 2,
            "backupCount": 2,
        },
        "uvicorn": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/uvicorn.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 2,
            "backupCount": 2,
        },
        "db": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/sql.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 4,
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "elasticapm": {
            "handlers": ["ecs"],
            "level": "WARNING",
        },
        "celery": {
            "handlers": ["celery"],
            "propagate": True,
            "level": "INFO",
        },
        "django": {
            "handlers": ["django"],
            "propagate": True,
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["db"],
            "propagate": True,
            "level": "DEBUG" if DEBUG else "WARNING",
        },
        "uvicorn": {
            "handlers": ["uvicorn"],
            "propagate": True,
            "level": "INFO",
        },
    },
}