import os
import sys

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
    # Added
    'storages',
    'widget_tweaks',
    'tinycontent',
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

# Authentication allauth "allauth.socialaccount"
INSTALLED_APPS += ["allauth", "allauth.account"]
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Config https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = os.environ.get(
    'ACCOUNT_AUTHENTICATION_METHOD', default='email')
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = int(os.environ.get(
    'ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS', default='3'))
ACCOUNT_EMAIL_REQUIRED = os.environ.get(
    'ACCOUNT_EMAIL_REQUIRED', default=True)
ACCOUNT_EMAIL_VERIFICATION = os.environ.get(
    'ACCOUNT_EMAIL_VERIFICATION', default=True)
ACCOUNT_UNIQUE_EMAIL = os.environ.get(
    'ACCOUNT_UNIQUE_EMAIL', default=True)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = os.environ.get(
    'ACCOUNT_LOGIN_ATTEMPTS_LIMIT', default=5)
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = os.environ.get(
    'ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION', default=True)
ACCOUNT_SESSION_REMEMBER = os.environ.get(
    'ACCOUNT_SESSION_REMEMBER', default=True)
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = os.environ.get(
    'ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE', default=False)
ACCOUNT_SIGNUP_FORM_CLASS = os.environ.get(
    'ACCOUNT_SIGNUP_FORM_CLASS')
ACCOUNT_USERNAME_REQUIRED = os.environ.get(
    'ACCOUNT_USERNAME_REQUIRED', default=False)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

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
# Restrict access to ALL todo lists/views to `is_staff` users.
# If False or unset, all users can see all views (but more granular permissions are still enforced
# within views, such as requiring staff for adding and deleting lists).
TODO_STAFF_ONLY = True

# If you use the "public" ticket filing option, to whom should these tickets be assigned?
# Must be a valid username in your system. If unset, unassigned tickets go to "Anyone."
TODO_DEFAULT_ASSIGNEE = "adrian@acrolama.com"

# If you use the "public" ticket filing option, to which list should these tickets be saved?
# Defaults to first list found, which is probably not what you want!
TODO_DEFAULT_LIST_SLUG = "tickets"

# If you use the "public" ticket filing option, to which *named URL* should the user be
# redirected after submitting? (since they can't see the rest of the ticket system).
# Defaults to "/"
TODO_PUBLIC_SUBMIT_REDIRECT = "home"

# Enable or disable file attachments on Tasks
# Optionally limit list of allowed filetypes
TODO_ALLOW_FILE_ATTACHMENTS = False
TODO_ALLOWED_FILE_ATTACHMENTS = [".jpg", ".gif", ".csv", ".pdf", ".zip"]
TODO_MAXIMUM_ATTACHMENT_SIZE = 5000000  # In bytes

# additionnal classes the comment body should hold
# adding "text-monospace" makes comment monospace
TODO_COMMENT_CLASSES = []

# The following two settings are relevant only if you want todo to track a support mailbox -
# see Mail Tracking below.
# TODO_MAIL_BACKENDS
# TODO_MAIL_TRACKERS
