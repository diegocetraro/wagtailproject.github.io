import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

DEBUG = False

SECRET_KEY = 'ns-x-r%+(g!fax27y(o55b821z)pgcx0sufb)%nz^*)1(q=c39'
ALLOWED_HOSTS = ['localhost','wagtailproject.learningwagtail.com','*']
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache" #CREATES .cache directory in current directory (os.getcwd())
    }
}

#********PostGreSQL SETUP************
DATABASES = {
    "Default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'wagtailproject',
        "USER": 'wagtailproject',
        "PASSWORD": '01101001..aB',
        "HOST": 'localhost',
        "PORT": ''
    }
}

sentry_sdk.init(
    dsn="https://46b12b097056470b8bb2ec2664c15bb1@o525013.ingest.sentry.io/5638408",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

#********PostGreSQL SETUP************

try:
    from .local import *
except ImportError:
    pass
