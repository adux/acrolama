import os
import sys
from acrolama.aws.conf import STATIC_URL, STATICFILES_STORAGE
from .base import BASE_DIR

COMPRESS_ENABLED = False
COMPRESS_CSS_HASHTAG_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = 'https:' + STATIC_URL
COMPRESS_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static/")
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
