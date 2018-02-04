# -*- coding: utf-8 -*-
"""Django settings for Github Contrib project."""

import os
import os.path as op
import sys

import raven

try:
    import local_settings
except ImportError:
    try:
        from . import initial_settings as local_settings
    except ImportError:  # pragma: no cover
        print('No initial settings!')
        sys.exit()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Debugging
DEBUG = local_settings.DEBUG
INTERNAL_IPS = local_settings.INTERNAL_IPS
DEBUG_TOOLBAR_PANELS = [
    # 'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    # 'debug_toolbar.panels.settings.SettingsPanel',
    # 'debug_toolbar.panels.headers.HeadersPanel',
    # 'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    # 'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

DATABASES = local_settings.DATABASES
WSGI_APPLICATION = 'ghcontrib_project.wsgi.application'
ROOT_URLCONF = 'ghcontrib_project.urls'
SECRET_KEY = local_settings.SECRET_KEY
ALLOWED_HOSTS = [local_settings.PROJECT_DOMAIN]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'rosetta',
    'social_django',
    'menu',
    'ghcontrib',
]
if DEBUG:  # pragma: no cover
    INSTALLED_APPS += [
        'debug_toolbar',
        'template_timings_panel',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:  # pragma: no cover
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Logging
RAVEN_CONFIG = {
    'dsn': local_settings.RAVEN_DSN,
    'release': raven.fetch_git_sha(local_settings.GIT_ROOT),
}
if not DEBUG:  # pragma: no cover
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': ('%(levelname)s %(asctime)s %(module)s '
                           '%(process)d %(thread)d %(message)s')
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {
                    'custom-tag': 'x'
                },
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'), ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
            ),
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug':
            DEBUG
        },
    },
]
if DEBUG:  # pragma: no cover
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]

# Static files
STATIC_ROOT = op.join(local_settings.PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = op.join(local_settings.PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Authentification
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
AUTH_USER_MODEL = 'ghcontrib.User'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Русский'),
)
LOCALE_PATHS = (op.join(local_settings.PROJECT_ROOT, 'project', 'locale'), )

# Loggin
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Social
SOCIAL_AUTH_GITHUB_KEY = local_settings.SOCIAL_AUTH_GITHUB_KEY
SOCIAL_AUTH_GITHUB_SECRET = local_settings.SOCIAL_AUTH_GITHUB_SECRET

GITHUB_API_KEY = local_settings.GITHUB_API_KEY

# This is here to fix the problem with static files on dev
try:
    from local_settings2 import *  # noqa pylint: disable=wildcard-import
except ImportError:
    pass
