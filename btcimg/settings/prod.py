import os

from . import django_compressor_manifest
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['btcimg.com']

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'FUCK55@55h_ulnhk60t)-u+bfwi64o=_5qi@-=_4%c^k7*3s3gy8v(LALL'

# CDN SHIT
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_OFFLINE_MANIFEST = django_compressor_manifest()

AWS_HEADERS = {
    'Expires': 'Sun, 19 Jul 2020 18:06:32 GMT'
}
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'lockboxlockbox'

DEFAULT_FILE_STORAGE = 'btcimg.settings.s3utils.MediaRootS3BotoStorage'
MEDIA_URL = 'https://s3-us-west-1.amazonaws.com/lockboxlockbox/media/'

STATICFILES_STORAGE = 'btcimg.settings.s3utils.StaticRootS3BotoStorage'
STATIC_URL = 'https://s3-us-west-1.amazonaws.com/lockboxlockbox/static/'
COMPRESS_STORAGE = STATICFILES_STORAGE
## end CDN SHIT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/btcimg/django.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
