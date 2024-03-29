import datetime
import os
from acrolama.settings.base import BASE_DIR

# Expiration Calc
two_months = datetime.timedelta(days=365)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

# Checks
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_S3_CUSTOM_DOMAIN = "d1j4p94w54mk15.cloudfront.net"
AWS_S3_SECURE_URLS = True

AWS_STORAGE_BUCKET_NAME = "acrolama"
STATICFILES_STORAGE = "acrolama.aws.utils.CachedS3Boto3Storage"
COMPRESS_STORAGE = STATICFILES_STORAGE

AWS_IS_GZIPPED = True

AWS_STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
COMPRESS_URL = STATIC_URL

STATIC_ROOT = "static"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = "public-read"
AWS_S3_REGION_NAME = "eu-central-1"
AWS_S3_OBJECT_PARAMETERS = {
    "Expires": expires,
    "CacheControl": "max-age=%d" % (int(two_months.total_seconds()),),
}

AWS_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
DEFAULT_FILE_STORAGE = "acrolama.aws.utils.MediaRootS3BotoStorage"

ADMIN_MEDIA_PREFI = STATIC_URL + "admin/"

# Compress test
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHTAG_METHOD = "content"
COMPRESS_CSS_FILTERS = ["compressor.filters.css_default.CssAbsoluteFilter", "compressor.filters.cssmin.CSSMinFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_PARSER = "compressor.parser.HtmlParser"
