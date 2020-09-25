import os
import sys

from .allauth import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Change of root of apps
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "apps/todo"))

MIDDLEWARE = [
    # 'django.middleware.gzip.GZipMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "acrolama.urls"
WSGI_APPLICATION = "acrolama.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # allauth needs this
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {"booking_tags": "apps.booking.templatetags.booking_tags", },
        },
    },
]

DJANGO_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",  # allauth
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",  # allauth
    "django.contrib.staticfiles",  # django debuger uses this
    "django.contrib.sites",  # allauth
    "django.contrib.sitemaps",
]

EXTERNAL_APPS = [
    "django_filters",
    "storages",
    "widget_tweaks",
    "tinycontent",
    "allauth",
    "allauth.account",
    "invitations",
]

LOCAL_APPS = ["home", "project", "address", "audiovisual", "accounting", "booking", "users"]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS

# Crispy Forms for todo
# INSTALLED_APPS += ["crispy_forms"]
# CRISPY_TEMPLATE_PACK = "bootstrap3"

# Analytica
INSTALLED_APPS += ["analytical"]
GOOGLE_ANALYTICS_PROPERTY_ID = "UA-118797477-1"

# Auth
AUTH_USER_MODEL = "users.User"
SITE_ID = 1  # required by allauth
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "acrolama"}}

# STATIC FILES AND COMPRESSION
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Audiovisual
IMAGE_SIZE = (os.environ.get("IMAGE_SIZE", default=(1170, 2240)),)
THUMB_SIZE = (os.environ.get("THUMB_SIZE", default=(800, 800)),)
MOB_SIZE = (os.environ.get("MOB_SIZE", default=(420, 420)),)


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True
