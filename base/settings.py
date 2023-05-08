"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.messages import constants as messages
import cloudinary
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e80ehznsgmkbl2kquz++$368we(mf@n98q-g14@vo8yq(^vgs4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'accounts',
    'main',
    
    'allauth',
    'phonenumber_field',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    "debug_toolbar",
    'cloudinary',
    'cloudinary_storage',
    'multiselectfield',
    "crispy_bootstrap5",
    'ckeditor'
]

SITE_ID=1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
STATIC_URL = 'static/'
MEDIA_URL='media/'

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'media')
]

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'railway',
            'USER': 'postgres',
            'PASSWORD': 'SAAaFS640WNnTT9TU9mI',
            'HOST': 'containers-us-west-185.railway.app',
            'PORT': '6857',
        }
    }

    CLOUDINARY_STORAGE={
        'CLOUD_NAME': 'dvqvtwria',
        'API_KEY': '931772247249532',
        'API_SECRET': 'jOIXfWMEkGVsN4N4IYgZyFGZmvA',
    }
    cloudinary.config( 
        cloud_name = "dvqvtwria", 
        api_key = "931772247249532", 
        api_secret = "jOIXfWMEkGVsN4N4IYgZyFGZmvA" 
        )
    DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'

    STATIC_URL='https://foreverinc.github.io/alkestatic_cdn/'

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    STATIC_ROOT=os.path.join(BASE_DIR,'static_cdn')
    MEDIA_ROOT=os.path.join(BASE_DIR,'media_cdn')


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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/







# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'foreverinc.dev@gmail.com'
EMAIL_HOST_PASSWORD = 'zpnobianfavxcqwv'
EMAIL_USE_TLS = True



MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

INTERNAL_IPS = [
    "127.0.0.1",
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '108603166313-dv0g4385u37vk46u8o91qi2hj4pdgvi6.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}
SOCIALACCOUNT_PROVIDERS = {
    'globus': {
        'SCOPE': [
            'openid',
            'profile',
            'email',
            'urn:globus:auth:scope:transfer.api.globus.org:all'
        ]
    }
}

ACCOUNT_MAX_EMAIL_ADDRESSES= 2
ACCOUNT_EMAIL_VERIFICATION ='none' #none #mandatory #optional
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_LOGOUT_REDIRECT_URL ='account_login'
LOGIN_REDIRECT_URL='home'
ACCOUNT_AUTHENTICATION_METHOD='username_email'
ACCOUNT_USERNAME_MIN_LENGTH =4


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"