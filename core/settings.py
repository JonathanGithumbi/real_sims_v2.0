"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from django.conf import settings
from importlib import import_module

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8y-ks$a%-86&fn&^#kxc_v=u)revm8(dq8*p3oaz98530tbem'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
TIME_ZONE = 'UTC'
LOGIN_REDIRECT_URL = '/student/list'
# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    
    
    'bootstrap_modal_forms',
    'widget_tweaks',
    'user_account',
    'grade',
    'student.apps.StudentConfig',
    'bill.apps.BillConfig',

    'fees_structure',
    'invoice.apps.InvoiceConfig',
    'academic_calendar',
    'payment.apps.PaymentConfig',
    'vendor',
    'item',
    'core',
    'dashboard',
    'django_quickbooks.apps.DjangoQuickbooksConfig',



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
                 os.path.join(
                     BASE_DIR, 'user_account/templates/user_account/'),
                 os.path.join(
                     BASE_DIR, 'user_account/templates/user_account/registration'),
                 os.path.join(BASE_DIR, 'templates')],
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
        'PASSWORD': 'Root123!@#',
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
STATICFILES_FINDERS = [
    # searches in STATICFILES_DIRS
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # searches in STATIC subfolder of each app
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
AUTH_USER_MODEL = 'user_account.User'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/user_account/login/'

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
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = "1t$nAB01033!@#"
EMAIL_HOST_USER = "jonathan.m.githumbi@gmail.com"
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# THESE ARE THE SETTINGS FOR DJANGO-QUICKBOOKS


DEFAULTS = {

    'UPDATE_PAUSE_SECONDS': 35,
    'MINIMUM_UPDATE_SECONDS': 15,
    'MINIMUM_RUN_EVERY_NSECONDS': 30,
    'MINIMUM_RUN_EVERY_NMINUTES': 15,

    'SESSION_MANAGER_CLASS': 'QBWEBSERVICE.session_manager.SessionManager',

    'REALM_MODEL_CLASS': 'QBWEBSERVICE.models.Realm',
    'REALM_SESSION_MODEL_CLASS': 'QBWEBSERVICE.models.RealmSession',
    'QBD_TASK_MODEL_CLASS': 'QBWEBSERVICE.models.QBDTask',

    'REALM_CONNECTION_DECORATOR': 'QBWEBSERVICE.decorators.base_realm_connection',

    'RESPONSE_PROCESSORS': (
        'QBWEBSERVICE.processors.CustomerQueryResponseProcessor',
        'QBWEBSERVICE.processors.CustomerModResponseProcessor',
        'QBWEBSERVICE.processors.CustomerAddResponseProcessor',
        'QBWEBSERVICE.processors.InvoiceQueryResponseProcessor',
        'QBWEBSERVICE.processors.InvoiceAddResponseProcessor',
        'QBWEBSERVICE.processors.InvoiceModResponseProcessor',
        'QBWEBSERVICE.processors.ItemServiceQueryResponseProcessor',
    ),

    'RABBITMQ_DEFAULT_HOST': 'localhost',
    'RABBITMQ_DEFAULT_USER': 'guest',
    'RABBITMQ_DEFAULT_PASS': 'guest',
    'RABBITMQ_DEFAULT_VHOST': '/',
    'RABBITMQ_DEFAULT_PORT': 5672,


    'APP_URL': 'http://localhost:8000/qwc/quickbooks-desktop/',
    'APP_SUPPORT': 'http://localhost:8000/qwc/quickbooks-desktop/support/',
    'APP_ID': '',
    'APP_NAME': 'Kings Educational Centre SIMS',
    'APP_DESCRIPTION': 'synchronises financial data from sims to quickbooks',
    'QB_TYPE': 'QBFS',
    'OWNER_ID': '{1ee58da6-3051-11ea-b499-9cda3ea7afc1}',

    'LOCAL_MODEL_CLASSES': {
        'Invoice': '',
        'Customer': '',
        # after understanding the default implementation, Round 2 of intergration is adding more classes, a
    }
}

IMPORT_STRINGS = (
    'RESPONSE_PROCESSORS',
    'SESSION_MANAGER_CLASS',
    'REALM_MODEL_CLASS',
    'REALM_SESSION_MODEL_CLASS',
    'QBD_TASK_MODEL_CLASS',
    'REALM_CONNECTION_DECORATOR',
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        module_path, class_name = val.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for Quickbooks Web Connector setting '%s'. %s: %s." \
              % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class QBWCSettings(object):
    """
    A settings object, that allows Quickbooks Web Connector settings to be accessed as properties.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'QBWC_SETTINGS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(
                "Invalid Quickbooks Web Connector setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        if attr == 'LOCAL_MODEL_CLASSES':
            for key, value in val.items():
                val[key] = import_from_string(value, value)

        setattr(self, attr, val)
        return val


qbwc_settings = QBWCSettings(None, DEFAULTS, IMPORT_STRINGS)
