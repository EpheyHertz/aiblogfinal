"""
Django settings for aiblog_app project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rn#n+*yldmwe&x)(1-4*^+uf2+68m0*1-8zwc=!3e$-9n9av@p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['aiblogfinal.onrender.com','127.0.0.1']
# ALLOWED_HOST=[]
# settings.py

AUTHENTICATION_BACKENDS = [
    'bloggenerator.backends.EmailBackend',  # Custom authentication backend
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bloggenerator',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aiblog_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
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

WSGI_APPLICATION = 'aiblog_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# postgresql://aibloggenerator_soundgift:5b64fdb33abb515dd0823c0456189aad5aff5733@kdj.h.filess.io:5433/aibloggenerator_soundgift

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DATABASE'),        # Fetch from .env file
        'USER': config('POSTGRES_USER'),            # Fetch from .env file
        'PASSWORD': config('POSTGRES_PASSWORD'),    # Fetch from .env file
        'HOST': config('POSTGRES_HOST'),            # Fetch from .env file
        
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config("DB_NAME"),  # Replace with your database name
#         'USER': config("DB_USER"),  # Replace with your database user
#         'PASSWORD': config("DB_PASSWORD"),  # Replace with your database password
#         'HOST': config("DB_HOST"),  # Replace with your database host (e.g., 'localhost' or an IP address)
#         'PORT': '3306',  # Default MySQL port is 3306
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
CSRF_TRUSTED_ORIGINS = [
    "https://aiblogfinal.onrender.com",
    
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

GEMINI_API_KEY = config('GEMINI_API_KEY')
AAI_API_KEY = config('AAI_API_KEY')

STATIC_URL = '/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# This setting informs Django of the URI path from which your static files will be served to users
# Here, they well be accessible at your-domain.onrender.com/static/... or yourcustomdomain.com/static/...
# STATIC_URL = '/static/'
# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL for serving media files
MEDIA_URL = '/media/'

# Path where media files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure the media directory exists. If not, create it.
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

LOGIN_URL ='/login/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# SMTP server details from environment variables
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = int(config('EMAIL_PORT', 587))
EMAIL_USE_TLS = config('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
CONTACT_EMAIL = config('CONTACT_EMAIL')


