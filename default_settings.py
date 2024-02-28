import os
from mongoengine import register_connection

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__))) + '/'

SECRET_KEY = None
HASHID_SECRET = None
HASHID_ADMIN_SALT = None
HASHID_PUBLIC_SALT = None
DEBUG = True
API_DOCUMENTATION = True
DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ["*"]

SITE_URL = 'just-try-it-out.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = None
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'django_hosts',
    'django_filters',
    'widget_tweaks',
    'django_tables2',
    'corsheaders',
    'rest_framework',
    'drf_yasg2',
    'ckeditor',
    'ckeditor_uploader',

    'core.Utils',
    'core.User',
]

AUTH_USER_MODEL = 'User.User'

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_DOMAIN = '.just-try-it-out.local'
SESSION_COOKIE_DOMAIN = '.just-try-it-out.local'

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_HOSTCONF = 'hosts'
DEFAULT_HOST = 'public'
ROOT_URLCONF = 'urls'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'core/templates/',
            BASE_DIR + 'core/Utils/templates/',
            BASE_DIR + 'Api/templates/',
            BASE_DIR + 'Admin/templates/',
            BASE_DIR + 'Public/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.Utils.context_processors.default_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'just_try_it_out',
        'USER': 'just_try_it_out',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE_DEFAULT = 'Europe/Kyiv'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR + 'static/'
MEDIA_ROOT = BASE_DIR + 'media/'
STATICFILES_DIRS = [
    BASE_DIR + 'htdocs/'
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'COERCE_DECIMAL_TO_STRING': False,
}
SWAGGER_SETTINGS = {
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24  # 24h

CKEDITOR_UPLOAD_PATH = BASE_DIR + 'media/ckeditoruploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '0'

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_RESULT_BACKEND = 'rpc'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_RESULT_EXPIRES = 60
CELERY_QUEUES = {
    'celery': {'exchange': 'celery',
               'exchange_type': 'direct',
               'durable': True},
}

ITEMS_PER_PAGE = 20

MONGODB_LOGGER_ALIAS = 'logger'
MONGODB_LOGGER_COLLECTION = 'log'
register_connection(alias=MONGODB_LOGGER_ALIAS,
                    host='mongodb://127.0.0.1:27017/just_try_it_out_logger',
                    w=0)
