import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from urllib.parse import urlparse

from .base import *
from acrolama.aws.conf import *

# General
# ------------------------------------------------------------------------------
ADMIN_URL = os.environ.get("DJANGO_ADMIN_URL")

ADMINS = (("Adrian Garate", "adrian@acrolama.com"),)

MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 's9+nemt@ka=)v2dsqwdQWDQWDQEQWRGQERVQWEFcu^##"w2#abu)v85)zh#ej2f2dqqwdq')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [
    "stageacrolama.herokuapp.com",
    "acrolama.herokuapp.com",
    "www.acrolama.com",
    "acrolama.com",
    ".acrolama.com",
]

# Collecting
# ------------------------------------------------------------------------------
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"

# Sentry SDK
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn="https://449183d07de2455ba0ecf384ca29a77f@sentry.io/1310482",
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
    ])

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["anymail"]
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": os.environ.get("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}

# Database for heroku
# ------------------------------------------------------------------------------
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# HTML MINIFY
# ------------------------------------------------------------------------------
MIDDLEWARE += ["htmlmin.middleware.HtmlMinifyMiddleware", "htmlmin.middleware.MarkRequestMiddleware"]

HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = True

# CACHES
# ------------------------------------------------------------------------------
redis_url = urlparse(os.environ.get("REDISCLOUD_URL"))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s" % (redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "PASSWORD": redis_url.password,
            "DB": 0,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}


# HTTPS
# ------------------------------------------------------------------------------
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
