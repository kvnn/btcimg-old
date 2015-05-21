from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'FUCK55@55h_ulnhk60t)-u+bfwi64o=_5qi@-=_4%c^k7*3s3gy8v(LALL'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = globals().get('INSTALLED_APPS', [])
INSTALLED_APPS += (
    'debug_toolbar',
)
