from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'btc51w-&=!oukvwe36vii9p-m11hs#vqgx$w(##8j7%xoj!sy)dv+img'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = globals().get('INSTALLED_APPS', [])
INSTALLED_APPS += (
    'debug_toolbar',
)
