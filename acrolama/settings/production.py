from .base import *
from .anymail import *
from acrolama.aws.conf import *

# For Heroku
import dj_database_url

INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"

INSTALLED_APPS += ["anymail"]

# Sentry SDK
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://449183d07de2455ba0ecf384ca29a77f@sentry.io/1310482",
    integrations=[DjangoIntegration()]
)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

ADMINS = (
    ('Adrian Garate', 'adrian@acrolama.com'),
)

MANAGERS = ADMINS

ADMIN_URL = os.environ.get('DJANGO_ADMIN_URL')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    's9+nemt@ka=)v2dsqwdQWDQWDQEQWRGQERVQWEFcu^##"w2#abu)v85)zh#ej2f2dqqwdq'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [
    'stageacrolama.herokuapp.com',
    'acrolama.herokuapp.com',
    'www.acrolama.com',
    'acrolama.com',
    '.acrolama.com'
]

# Database for heroku
# import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500

# HTML MINIFY
MIDDLEWARE += [
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware'
]

HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = True

# Secure
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
