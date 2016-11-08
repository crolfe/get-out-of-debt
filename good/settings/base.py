"""
Django settings for Get Out of Debt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


def local_path(path):
    return os.path.join(BASE_DIR, path)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xt*t8b7fc$fw_k@m1ua6k&t8q^ch6h+6!^^@k9!=n&kfct51+h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'pipeline'
)

PROJECT_APPS = (
    'loans',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE_CLASSES = (
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
        'NAME': local_path('db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [local_path('templates')],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages'],
    },
}]

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder'
)
STATICFILES_DIRS = (
    local_path('resources'),
)
STATIC_ROOT = local_path('static')
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE = {
    'STYLESHEETS': {
        'vendor': {
            'source_filenames': ('css/foundation.css',),
            'output_filename': 'loans/css/vendor.css'
        },
        'loans': {
            'source_filenames': ('loans/css/loans.css',),
            'output_filename': 'loans/css/app.css'
        }
    },
    'JAVASCRIPT': {
        'vendor': {
            'source_filenames': (
                'js/bower_components/chart.js/dist/Chart.js',
                'js/bower_components/angular/angular.js',
                'js/bower_components/angular-sanitize/angular-sanitize.js',
                ('js/bower_components/angular-ui-router'
                 '/release/angular-ui-router.js'),
                'js/bower_components/angular-foundation/mm-foundation-tpls.js',
                'js/bower_components/moment/moment.js',
                ('js/bower_components/tc-angular-chartjs/dist/'
                 'tc-angular-chartjs.js'),
            ),
            'output_filename': 'js/vendor.js'
        },
        'loans': {
            'source_filenames': (
                'js/app.js',
                'js/services/APIService.js',
                'js/controllers/chartCtrl.js',
            ),
            'output_filename': 'js/loans-app.js'
        },
        'shims': {
            'source_filenames': (
                'js/bower_components/json3/lib/json3.min.js',
                'js/bower_components/es5-shim/es5-shim.js'
            ),
            'output_filename': 'js/shims.js'
        }
    }
}

# npm install -g uglify-js
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.NoopCompressor'
