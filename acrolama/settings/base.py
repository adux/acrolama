import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Change of root of apps
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

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
                'django.template.context_processors.request', #allauth needs this
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', #allauth
    'django.contrib.contenttypes',
#   'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages', #allauth
    'django.contrib.staticfiles', # django debuger uses this
    'django.contrib.sites', #allauth
    #Added
    'storages',
    'widget_tweaks',
    'django_filters',
    #Own
    'home',
    'project',
    'address',
    'audiovisual',
    'accounting',
    'booking',
    'users'
]

SITE_ID = 1 #required by allauth

#Crispy Forms for todo
INSTALLED_APPS += ["crispy_forms"]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#Analytica
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

# Authentication allauth
INSTALLED_APPS += ["allauth", "allauth.account", "allauth.socialaccount"]
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Todo-specific settings
INSTALLED_APPS += ["todo"]
TODO_DEFAULT_LIST_ID = None
# Restrict access to todo lists/views to `is_staff()` users.
# False here falls back to `is_authenticated()` users.
TODO_STAFF_ONLY = True

# If you use the "public" ticket filing option, to whom should these tickets be assigned?
# Must be a valid username in your system. If unset, unassigned tickets go to "Anyone."
TODO_DEFAULT_ASSIGNEE = None

# If you use the "public" ticket filing option, to which list should these tickets be saved?
# Defaults to first list found, which is probably not what you want!
TODO_DEFAULT_LIST_SLUG = 'tickets'

# If you use the "public" ticket filing option, to which *named URL* should the user be
# redirected after submitting? (since they can't see the rest of the ticket system).
# Defaults to "/"
TODO_PUBLIC_SUBMIT_REDIRECT = '/'
