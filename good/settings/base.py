# -*- coding: utf-8 -*-
"""
Django settings for Get Out of Debt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xt*t8b7fc$fw_k@m1ua6k&t8q^ch6h+6!^^@k9!=n&kfct51+h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'south',
    'rest_framework',
    'corsheaders',
    'djangular',
    'pipeline'
)

PROJECT_APPS = (
    'loans',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'good.urls'

WSGI_APPLICATION = 'good.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    (os.path.abspath(os.path.join(BASE_DIR, 'templates')))
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangular.finders.NamespacedAngularAppDirectoriesFinder'
)

STATICFILES_DIRS = (
    os.path.abspath(os.path.join('..', BASE_DIR, 'resources')),
)

STATIC_ROOT = os.path.abspath(os.path.join('..', BASE_DIR, 'static'))

CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# sudo npm install -g cssmin
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = '/usr/bin/env cssmin'
PIPELINE_CSSMIN_ARGUMENTS = ''

# npm install -g uglify-js
# We use uglify instead of yuglify otherwise jQuery blows up
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_UGLIFYJS_BINARY = '/usr/bin/env uglifyjs'
PIPELINE_UGLIFYJS_ARGUMENTS = ''

PIPELINE_CSS = {
    'loans_vendor': {
        'source_filenames': (
            'loans/css/foundation.css',
            'loans/bower_components/ng-grid/ng-grid.css',
        ),
        'output_filename': 'loans/css/vendor.css'
    },
    'loans': {
        'source_filenames': (
            'loans/styles/main.css',
        ),
        'output_filename': 'loans/css/app.css'
    }
}
PIPELINE_JS = {
    'loans_vendor': {
        'source_filenames': (
            'loans/bower_components/jquery/dist/jquery.js',
            'loans/bower_components/angular/angular.js',
            'loans/bower_components/angular-sanitize/angular-sanitize.js',
            'loans/bower_components/angular-ui-router/release/angular-ui-router.js',
            'loans/bower_components/angular-foundation/mm-foundation-tpls.js',
            'loans/bower_components/ng-grid/build/ng-grid.js',
            'loans/bower_components/moment/moment.js',
            'loans/bower_components/chartjs/Chart.min.js',
            'loans/js/angular-chartjs.js',
        ),
        'output_filename': 'loans/js/vendor.js'
    },
    'loans': {
        'source_filenames': (
            'loans/js/app.js',
            'loans/js/services/APIService.js',
            'loans/js/controllers/chartCtrl.js',
        ),
        'output_filename': 'loans/js/loans-app.js'
    },
    'shims': {
        'source_filenames': (
            'loans/bower_components/json3/lib/json3.min.js',
            'loans/bower_components/es5-shim/es5-shim.js'
        ),
        'output_filename': 'loans/js/shims.js'
    }
}