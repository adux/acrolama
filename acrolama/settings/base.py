import os
import sys

from .allauth import *
from .todo import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Change of root of apps
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps/todo'))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acrolama.urls'
WSGI_APPLICATION = 'acrolama.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # allauth needs this
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # allauth
    'django.contrib.contenttypes',
    # 'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',  # allauth
    'django.contrib.staticfiles',  # django debuger uses this
    'django.contrib.sites',  # allauth
    # Utils
    'django_filters',
    'storages',
    'widget_tweaks',
    'tinycontent',
    'todo',
    'allauth',
    'allauth.account',
    # Own
    'home',
    'project',
    'address',
    'audiovisual',
    'accounting',
    'booking',
    'users'
]

AUTH_USER_MODEL = "users.User"
SITE_ID = 1  # required by allauth

# Crispy Forms for todo
INSTALLED_APPS += ["crispy_forms"]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Analytica
INSTALLED_APPS += ["analytical"]
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-118797477-1'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'acrolama'
    }
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

