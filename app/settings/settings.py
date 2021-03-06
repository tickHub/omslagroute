import os
from os.path import join
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from keycloak_oidc.default_settings import *
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',            # utilities for rest apis
    'rest_framework.authtoken',  # TODO: remove once all user management is done using Grip
    'django_filters',            # for filtering rest endpoints
    'drf_yasg',                  # for generating real Swagger/OpenAPI 2.0 specifications
    'constance',
    'constance.backends.database',  # for dynamic configurations in admin
    'mozilla_django_oidc',       # for authentication
    'webpack_loader',
    'multiselectfield',
    'keycloak_oidc',

    'web.core',
    'web.documents',
    'web.timeline',
    'web.users',
    'web.organizations',
    'web.roles',
    'web.cases',
    'web.profiles',
    'web.forms',
    'web.feedback',

)
SOURCE_COMMIT = os.environ.get('COMMIT_HASH')
BRANCH_NAME = os.environ.get('BRANCH_NAME')

# https://docs.djangoproject.com/en/2.0/topics/http/middleware/
MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = os.environ.get('DJANGO_ROOT_URLCONF', 'web.urls')


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local')
WSGI_APPLICATION = 'wsgi.application'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")

ADMINS = (
    ('admin', 'maurice@mgui.nl'),
)

AUTH_USER_MODEL = 'users.User'


# Database
DEFAULT_DATABASE_NAME = 'default'

if os.environ.get('DATABASE_NAME'):
    DATABASES = {
        DEFAULT_DATABASE_NAME: {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST', 'database'),
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        DEFAULT_DATABASE_NAME: {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# General
APPEND_SLASH = True
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'nl-nl'
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'media'))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web.core.context_processors.app_settings',
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #     ]),
            # ],
        },
    },
]


# Password Validation
# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    )
}

# Mail
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS and allowed hosts
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')
CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGIN_WHITELIST', '').split(',')
CORS_ORIGIN_ALLOW_ALL = False

AUTH_GROUPNAME_PROCESS = 'proces'

LOGIN_URL = '/#login'

SWAGGER_SETTINGS = {
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/'
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ALLOW_DATA_ACCESS_KEY = 'ALLOW_DATA_ACCESS'
CONSTANCE_BRK_AUTHENTICATION_TOKEN_KEY = 'BRK_AUTHENTICATION_TOKEN'
CONSTANCE_BRK_AUTHENTICATION_TOKEN_EXPIRY_KEY = 'BRK_AUTHENTICATION_TOKEN_EXPIRY'
CONSTANCE_HOMEPAGE_INTRO_KEY = 'HOMEPAGE_INTRO'
CONSTANCE_FEEDBACK_RECIPIENT_LIST_KEY = 'FEEDBACK_RECIPIENT_LIST'

CONSTANCE_CONFIG = {
    CONSTANCE_ALLOW_DATA_ACCESS_KEY: (True, 'Allow data to be accesible through the API'),
    CONSTANCE_BRK_AUTHENTICATION_TOKEN_KEY: ('', 'Authentication token for accessing BRK API'),
    CONSTANCE_BRK_AUTHENTICATION_TOKEN_EXPIRY_KEY: ('', 'Expiry date for BRK API token'),
    CONSTANCE_HOMEPAGE_INTRO_KEY: ('', 'Homepage introduction html'),
    CONSTANCE_FEEDBACK_RECIPIENT_LIST_KEY: ('', 'Feedback ontvangers lijst(kommagescheiden)'),
}

# AUTHENTICATION_BACKENDS = [
#     'keycloak_oidc.auth.OIDCAuthenticationBackend',
# ]

OIDC_RP_CLIENT_ID = os.environ.get('IAM_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.environ.get('IAM_CLIENT_SECRET')

# OIDC_OP_LOGOUT_URL_METHOD = 'api.users.utils.oidc_op_logout'
# OIDC_USERNAME_ALGO = 'api.users.utils.generate_username'
# OIDC_RP_SIGN_ALGO = 'RS256'
# OIDC_RP_SCOPES = 'openid'
# OIDC_USE_NONCE = False

if os.environ.get("IAM_URL"):
    IAM_URL = os.environ.get('IAM_URL', 'https://iam.amsterdam.nl/auth/realms/datapunt-acc/protocol/openid-connect/')
    OIDC_OP_AUTHORIZATION_ENDPOINT = urllib.parse.urljoin(IAM_URL, 'auth')
    OIDC_OP_TOKEN_ENDPOINT = urllib.parse.urljoin(IAM_URL, 'token')
    OIDC_OP_USER_ENDPOINT = urllib.parse.urljoin(IAM_URL, 'userinfo')
    OIDC_OP_JWKS_ENDPOINT = urllib.parse.urljoin(IAM_URL, 'certs')
    OIDC_OP_LOGOUT_ENDPOINT = urllib.parse.urljoin(IAM_URL, 'logout')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    }
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    # We don't refresh tokens yet, so we set refresh lifetime to zero
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=0),
}

ACCESS_LOG_EXEMPTIONS = (
    '/state/health',
)

# BRK Access request settings
BRK_ACCESS_CLIENT_ID = os.getenv('BRK_ACCESS_CLIENT_ID')
BRK_ACCESS_CLIENT_SECRET = os.getenv('BRK_ACCESS_CLIENT_SECRET')
BRK_ACCESS_URL = os.getenv('BRK_ACCESS_URL')
BRK_API_OBJECT_EXPAND_URL = 'https://acc.api.data.amsterdam.nl/brk/object-expand/'

BAG_API_SEARCH_URL = 'https://api.data.amsterdam.nl/atlas/search/adres/'

# swift storage
if os.environ.get("SWIFT_AUTH_URL"):
    SWIFT_BASE_URL = 'https://%s.%s' % (os.environ.get("SWIFT_PROJECT_ID"), os.environ.get("SWIFT_EXTERNAL_DOMAIN"))
    SWIFT_AUTH_URL = os.environ.get("SWIFT_AUTH_URL")
    SWIFT_USERNAME = os.environ.get("SWIFT_USER")
    SWIFT_PASSWORD = os.environ.get("SWIFT_PASSWORD")
    SWIFT_TENANT_ID = os.environ.get("SWIFT_TENANT")
    SWIFT_TEMP_URL_KEY = os.environ.get("SWIFT_TEMP_URL_KEY")
    SWIFT_TEMP_URL_DURATION = os.environ.get("SWIFT_TEMP_URL_DURATION", 30)

    SWIFT_USE_TEMP_URLS = os.environ.get("SWIFT_USE_TEMP_URLS", 'True') == 'True'
    SWIFT_CONTAINER_NAME = os.environ.get("SWIFT_CONTAINER_NAME", 'media')
    DEFAULT_FILE_STORAGE = 'web.core.storage.SwiftStorage'
    THUMBNAIL_DEFAULT_STORAGE = 'web.core.storage.SwiftStorage'

    CORS_ORIGIN_WHITELIST = [SWIFT_BASE_URL, ]
