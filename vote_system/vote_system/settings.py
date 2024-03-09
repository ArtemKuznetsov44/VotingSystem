"""
Django settings for vote_system project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d&&phu2n_8)k+xcz4iuf10hq_tcm)yc^v#)(r(07#i)7vjq_%2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts for running our project:
ALLOWED_HOSTS = ['127.0.0.1', '172.20.10.6']

#
AUTH_USER_MODEL = "users.User"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # We need to specify name of our application or, and it is better to use,
    # we can specify class - absolute path:
    'users.apps.UsersConfig',
    'main.apps.MainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vote_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Config to get base.html file from templates directory in our base project dir - vote_system:
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Here we can enable our own contex processors. Context processor, as we can understand by name,
                # are used for bring some context data for templates, but such files after its registration here we
                # can use anywhere we want in our project: By patient, try only to use them in cases when practically
                # all pages in project should be with context, which context processor provide (just a menu titles
                # and links, as example).
                'main.context_processor.get_context_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'vote_system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artem',
        'USER': 'artem',
        'PASSWORD': '1802',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# We can specify to use RUSSIAN language as the main language in current django project
# Especially it works with admin panel:
# LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Static prefix for static filed in our project:
STATIC_URL = 'static/'

# If we need to use not only static files from folders in current apps, we can specify
# another paths for static files. For example, here I enable static directory for our base.html file.
# This folder all in all will be the main static files dir for our project after running it not in debug config.
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Main media directory path for our project (not for app, this folder is common for each application):
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Media prefix for url:
MEDIA_URL = '/media/'

# The default url address which is used by django to redirect user after its logout:
LOGOUT_REDIRECT_URL = 'start'
LOGIN_URL = 'users:sign_in'

# Authentication backends should be specified in such order: firstly - default backend process, and only after it, we
# can specify our backend.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Our authentication class. With it, we can be authenticated as user not only by username, but with email too:
    'users.authentication.EmailAuthBackend'
]
