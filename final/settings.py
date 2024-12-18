"""
Django settings for final project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import ssl
from elasticsearch_dsl import connections
import tensorflow as tf
import logging
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
# TensorFlow 로그 레벨 설정
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
tf.get_logger().setLevel(logging.ERROR)
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/



SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'blog.middleware.LogOnlyLoggedInMiddleware', # 로그인 한 유저만 로그 수집 가능하게 하는 미들웨어
    'blog.middleware.UserActionLoggingMiddleware', # 페이지가 넘어갈 때 로그가 남을 수 있도록 하는 미들웨어
]


ROOT_URLCONF = "final.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'accounts', 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "final.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

'''DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}'''

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME":  os.getenv('NAME'),
        "PORT":  os.getenv('PORT'),
        "PASSWORD":  os.getenv('PASSWD'),
        "HOST":  os.getenv('HOST'),
        "USER":  os.getenv('USER'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'"
            }                                                    # STRICT_TRANS_TABLES: 트랜잭션을 지원하는 테이블, 
                                                                  # 잘못된 데이터가 삽입되거나 업데이트될 때 경고 대신 오류를 발생
    }
}

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
# img나 이런것들을 static 폴더에서 받아 오게 하기위해서
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",  # 또는 os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# Elasticsearch 연결 설정
connections.create_connection(alias="default", hosts=[os.getenv('ES')])

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv('ES')
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # 예: Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL')  # 발신자 이메일
EMAIL_HOST_PASSWORD = os.getenv('EMAILPASSWD')  # 발신자 이메일 비밀번호
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MODEL_PATH = os.path.join(BASE_DIR, 'models', 'customer_income_model.h5')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',  # WARNING 이하 메시지 숨김
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',  # WARNING 이하 메시지 숨김
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}