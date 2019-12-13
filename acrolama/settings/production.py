from .base import *
# Media and Static Files for production
from acrolama.aws.conf import *
# For Heroku
import dj_database_url

# Sentry SDK
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://449183d07de2455ba0ecf384ca29a77f@sentry.io/1310482",
    integrations=[DjangoIntegration()]
)

# Anymail (Mailgun)
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa F405
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_DOMAIN'),
    "MAILGUN_API_URL": os.environ.get('MAILGUN_API_URL', default='https://api.mailgun.net/v3'),
}

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

ADMINS = (
    ('Adrian Garate', 'adrian@acrolama.com'),
)
MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 's9+nemt@ka=)v2dsqwdQWDQWDQEQWRGQERVQWEFcu^##"w2#abu)v85)zh#ej2f2dqqwdq')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['stageacrolama.herokuapp.com', 'acrolama.herokuapp.com', 'www.acrolama.com', 'acrolama.com', '.acrolama.com']

# Database for heroku
# import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

# HTML MINIFY
MIDDLEWARE += [
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware'
]
HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = True

INSTALLED_APPS += ["compressor"]
COMPRESS_ENABLED = False
COMPRESS_CSS_HASHTAG_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_URL = S3_URL
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
COMPRESS_URL = 'https:' + STATIC_URL

# Admin URL
ADMIN_URL = os.environ.get('DJANGO_ADMIN_URL')

# Secure
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
