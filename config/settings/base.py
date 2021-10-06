import os

import      configparser
from        decouple            import config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

#
# AUTH_USER_MODEL = 'accounts.CustomUser'
#
# AUTHENTICATION_BACKENDS = ('config.backends.AuthBackend',)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # API - Apps
    'rest_framework',
    'rest_framework.authtoken',

    # Third Party Apps
    'django_countries',
    'crispy_forms',
    'bootstrap4',
    'django_user_agents',
    'dal',
    'dal_select2',

    # Project app
    'pcshop.apps.web.store',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# DRF Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

LOGIN_REDIRECT_URL = '/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pcshop/templates',)],
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

WSGI_APPLICATION = 'config.wsgi.application'

#Database
CONFIG_DIR = os.path.join(BASE_DIR, 'config/')

parser = configparser.ConfigParser()

parser.read_file(open(os.path.join(CONFIG_DIR, 'app.ini')))

#Done with postgresql
DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql',
        'NAME'      : parser.get('pcshop_dev', 'HP_DB_NAME'),
        'USER'      : parser.get('pcshop_dev', 'HP_DB_USER'),
        'PASSWORD'  : parser.get('pcshop_dev', 'HP_DB_PASSWORD'),
        'HOST'      : parser.get('pcshop_dev', 'HP_DB_HOST') or '127.0.0.1',
        'PORT'      : parser.getint('pcshop_dev', 'HP_DB_PORT') or '5432',

    }
}


# # gmail
EMAIL_BACKEND   = config('EMAIL_BACKEND')
EMAIL_HOST      = config('EMAIL_HOST')
EMAIL_USE_TLS   = config('EMAIL_USE_TLS')
EMAIL_PORT      = config('EMAIL_PORT')
EMAIL_SENDER    = config('EMAIL_SENDER')
#EMAIL_HOST_USER = config('EMAIL_HOST_USER')# test with registration reset
EMAIL_PASSWORD  = config('EMAIL_PASSWORD')

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE       = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
BASE_PATH = os.path.join(BASE_DIR)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pcshop/static')]

STATIC_URL  = '/static/'

STATIC_ROOT = os.path.join(BASE_PATH, 'pcshop/static/includes')

MEDIA_URL   = '/media/'

MEDIA_ROOT  = os.path.join(BASE_PATH, 'pcshop/static/media')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'