import os

INSTALLED_APPS += ["compressor"]
COMPRESS_ENABLED = False
COMPRESS_CSS_HASHTAG_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_URL = S3_URL
COMPRESS_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
COMPRESS_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
COMPRESS_URL = 'https:' + STATIC_URL
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
