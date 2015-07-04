"""
Django settings for test_project project.

Generated by 'django-admin startproject' using Django dev.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j2i1*i)uh*-&cdn^+0*i3^cw9gx-^jrc2&yfn!o-xy)$ij154j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'testolwidget',
    'olwidget',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testolwidget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'testolwidget.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

POSTGIS_TEMPLATE = 'template_postgis'
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'olwidget_dev',
        'USER': 'django_dev',
        'PASSWORD': 'django_dev',
    }
}


# Password validation
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# localhost:8000
GOOGLE_API_KEY = 'ABQIAAAARaukg-vCnyMKCmf7W1mdOhQCULP4XOMyhPd8d_NrQQEO8sT8XBTLlWMmpTlKIHpKhd2GXLaZc6gHJA'
# 18.85.23.189:8000
# GOOGLE_API_KEY = "ABQIAAAARaukg-vCnyMKCmf7W1mdOhTUM1TfCWCpQbByeYgbUi08Ugq4ShQ2qaNvdgbJz36kf2mKYgbUTR6R7A"
# olwidget documentation
YAHOO_APP_ID = 'JNrvOMXV34Ft.LUs2zzCI9yVPrIX1KDJ1tiNHFam9mLWl64qgtbSjenTP.ua1UWbPCbp0w6r.A--'

OLWIDGET_DEFAULT_OPTIONS = {
    'layers': ['osm.mapnik'],
}