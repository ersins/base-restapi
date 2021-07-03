from datetime import timedelta
from pathlib import Path
from .key_config import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SecretsEnv.SECRET_KEY  # 'django-insecure-(z@8k^vrwd2&qk$j0*vbbjxkk)e8a=ne*q!qi&xhivj+%jw_$^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DebugEnv.DEDUG

ALLOWED_HOSTS = AllowedHostEnv.ALLOWED_HOSTS

# Eposta Gönderim ayarları

EMAIL_HOST = EpostaEnv.EMAIL_HOST
EMAIL_HOST_USER = EpostaEnv.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EpostaEnv.EMAIL_HOST_PASSWORD
EMAIL_PORT = EpostaEnv.EMAIL_PORT
EMAIL_USE_TLS = EpostaEnv.EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = 'Klikya eCommerce <esenzek@gmail.com>'
BASE_URL = '127.0.0.1:8000'
MANAGERS = (
    ('Ersin Senzek', "ersinsenzek@gmail.com"),
)
ADMINS = MANAGERS

# User activation Süresi 7 olarak ayarlandı

DEFAULT_ACTIVATION_DAYS = 7

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt',
    'rest_framework',
    'django_filters',

    'authority',
    'todos.apps.TodosConfig',
]

AUTH_USER_MODEL = 'authority.User'  # changes the built-in user model to ours

# Redis url
# CELERY_BROKER_URL = 'amqp://esmayan:1qazxsw234@localhost:5672/pydev-vhost'
CELERY_BROKER_URL = CeleryEnv.CELERY_BROKER
CELERY_RESULT_BACKEND = CeleryEnv.CELERY_BACKEND

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RequestMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': FolderRoots.get_template_dirs(BASE_DIR),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': DatabaseEnv.NAME,
        'USER': DatabaseEnv.USER,
        'PASSWORD': DatabaseEnv.PASSWORD,
        'HOST': DatabaseEnv.HOST,
        'PORT': DatabaseEnv.PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'authority.jwt.JwtAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'NON_FIELD_ERRORS_KEY': 'error',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 10
    # 'DEFAULT_PAGINATION_CLASS': 'todos.pagination.CustomPageNumberPagination', 'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    FolderRoots.get_staticfiles_root(BASE_DIR),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# IMPORT_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "import_root")

STATIC_ROOT = FolderRoots.get_static_root(BASE_DIR)

MEDIA_URL = '/media/'
MEDIA_ROOT = FolderRoots.get_media_root(BASE_DIR)

PROTECTED_ROOT = FolderRoots.get_protected_root(BASE_DIR)
