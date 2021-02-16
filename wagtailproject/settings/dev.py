from .base import *
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f@r+2-f&810fq)5dusou6gqbtaf8_s+urbtgi_q-d!f@8ls9q6'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#******************FOR DJANGO DEBUG TOOLBAR***********************
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
#******************FOR DJANGO DEBUG TOOLBAR***********************


#******************SET CAHE SETTINGS******************************
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache" #CREATES .cache directory in current directory (os.getcwd())
    }
}

#******************SET CAHE SETTINGS******************************
try:
    from .local import *
except ImportError:
    pass
