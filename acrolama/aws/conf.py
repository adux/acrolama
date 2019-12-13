import datetime
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'acrolama.aws.utils.MediaRootS3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'acrolama'
AWS_S3_REGION_NAME = 'eu-central-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = S3_URL + 'media/'
MEDIA_ROOT = MEDIA_URL

STATIC_URL = S3_URL + 'static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

STATICFILES_STORAGE = 'acrolama.aws.utils.CachedS3BotoStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': expires,
    'CacheControl': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
