import      dj_database_url
from        .base               import *


DEBUG               = config('DEBUG')

ALLOWED_HOSTS       = ['127.0.0.1' , '' ]

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

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

# Honor the 'X-Forwarded-Proto' header fro request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)


# Static files (CSS, JavaScript, Images)
BASE_PATH = os.path.join(BASE_DIR)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pcshop/store/static')]

STATIC_URL  = '/static/'

STATIC_ROOT = os.path.join(BASE_PATH, 'pcshop/store/static/includes')

MEDIA_URL   = '/media/'

MEDIA_ROOT  = os.path.join(BASE_PATH, 'pcshop/store/static/media')

STATICFILES_STORAGE     = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ENVIRONMENT = 'PRODUCTION'

print("\n")
print("DEBUG        = ", DEBUG      )
print("MODE         = ", ENVIRONMENT)
print("STATIC_ROOT  = ", STATIC_ROOT)
print("MEDIA_ROOT   = ", MEDIA_ROOT )
print("\n")