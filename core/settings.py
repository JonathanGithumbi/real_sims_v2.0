"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8y-ks$a%-86&fn&^#kxc_v=u)revm8(dq8*p3oaz98530tbem'

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
    'user_account',
    'dashboard',
    'grade',
    'student',
    'bill',
    'fees_structure',
    'invoice',
    'academic_calendar',
    'report',
    'payment',
    'vendor',
    'account',
    'item',
    'bill_payment',
    'django_select2'
]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
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
        'DIRS': [os.path.join(BASE_DIR, 'global_template/'),
                 os.path.join(BASE_DIR, 'user_account/templates/user_account/'),
                 os.path.join(BASE_DIR, 'user_account/templates/user_account/registration')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sims_v2.0',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
AUTH_USER_MODEL = 'user_account.User'
LOGOUT_REDIRECT_URL = '/'
# OAauth2 config here
CLIENT_ID = 'ABqj7EU6zlngD2KKw34dy6Z7SzVwF7XcHP7c6EOr2GCZUiSOZI'
CLIENT_SECRET = 'KgY50RPimjKkz4shvDb2PRrIKADSadw8ysWIuOhA'
REDIRECT_URI = 'http://localhost:8000/user_account/callback'
ENVIRONMENT = 'sandbox'

# QBO Base URLs
QBO_BASE_SANDBOX = 'https://sandbox-quickbooks.api.intuit.com'
QBO_BASE_PROD = 'https://quickbooks.api.intuit.com'

# OAuth1 config for migration
CONSUMER_KEY = '<EnterHere>'
CONSUMER_SECRET = '<EnterHere>'
ACCESS_KEY = '<EnterHere>'
ACCESS_SECRET = '<EnterHere>'

REALM_ID = '<EnterHere>'

ALLOWED_HOSTS = ["http://127.0.0.1:8000/", '127.0.0.1', 'localhost']
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
AUTHENTICATION_BACKENDS = ['user_account.backends.AuthBackend']
DEFAULT_FROM_EMAIL = "jonathan.m.githumbi@gmail.com"
# EMAIL_HOST =
# EMAIL_PORT =
# EMAIL_HOST_PASSWORD=
# EMAIL_HOST_USER =
# EMAIL_PORT =
