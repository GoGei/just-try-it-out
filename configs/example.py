from default_settings import *

SECRET_KEY = 'super_secret_key'
HASHID_SECRET = 'super_secret_key'
DEBUG = True
API_DOCUMENTATION = True
DEBUG_TOOLBAR = False

TEMPLATES[0]['OPTIONS']['debug'] = True

SITE_URL = 'just-try-it-out.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = '4482'
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

DATABASES['default']['PASSWORD'] = 'your_db_password'

EMAIL_HOST_USER = 'user@example.com'
DEFAULT_FROM_EMAIL = 'user@example.com'
EMAIL_HOST_PASSWORD = 'email-hash-secret'

if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
