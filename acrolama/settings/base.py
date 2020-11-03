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
    "tinymce",
    "crispy_forms",
    "storages",
    "widget_tweaks",
    "tinycontent",
    "allauth",
    "allauth.socialaccount",
    "allauth.account",
    "invitations",
]

LOCAL_APPS = ["home", "project", "address", "audiovisual", "accounting", "booking", "users"]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS

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

# Sizes
IMAGE_SIZE = (os.environ.get("IMAGE_SIZE", default=(1170, 2240)),)
THUMB_SIZE = (os.environ.get("THUMB_SIZE", default=(800, 800)),)
MOB_SIZE = (os.environ.get("MOB_SIZE", default=(420, 420)),)

# TinyMCE
TINYMCE_COMPRESSOR = False
TINYMCE_INCLUDE_JQUERY = False
TINYMCE_DEFAULT_CONFIG = {
    'gecko_spellcheck': "true",
    'browser_spellcheck': "true",
    'height': "300",
    'selector': "textarea",
    'resize': "false",
    'autosave_ask_before_unload': "false",
    'powerpaste_allow_local_images': "true",
    'plugins': [
        'fullscreen autolink help image imagetools ',
        'link noneditable preview lists',
        'searchreplace'
    ],
    'toolbar':
        "insertfile undo redo | cut copy paste | formatselect bold italic | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist | link image | fullscreen preview searchreplace",
    'toolbar_mode': "sliding",
    'contextmenu': "false",
    'menubar': "false",
    'language': "de",
    'lists_indent_on_tab': "false"
}


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True
