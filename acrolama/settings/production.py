from .base import *
from acrolama.aws.conf import *

#Email
EMAIL_HOST = 'mail.gandi.net'
EMAIL_HOST_USER = 'web@acrolama.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Acrolama <web@acrolama.com>'
ADMINS = (
    ('adrian', 'adrian@acrolama'),
)
MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 's9+nemt@ka=)v2dsqwdQWDQWDQEQWRGQERVQWEFcu^##"w2#abu)v85)zh#ej2f2dqqwdq')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['stageacrolama.herokuapp.com', 'acrolama.herokuapp.com', 'www.acrolama.com', 'acrolama.com', '.acrolama.com']

# Database for heroku
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
#DATABASES['default']['CONN_MAX_AGE'] = 500

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

#Admin URL
ADMIN_URL = os.environ.get('DJANGO_ADMIN_URL')

#### Secure
CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True
