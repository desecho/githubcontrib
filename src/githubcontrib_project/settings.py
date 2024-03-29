"""Django settings for GitHubContrib project."""

from os import getenv
from os.path import abspath, dirname, join

import django_stubs_ext
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from githubcontrib.types import TemplatesSettings

django_stubs_ext.monkeypatch()

SENTRY_TRACE_SAMPLING = 0.5

sentry_sdk.init(  # pylint: disable=abstract-class-instantiated
    dsn=getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=SENTRY_TRACE_SAMPLING,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# Custom
IS_DEV = bool(getenv("IS_DEV"))
COLLECT_STATIC = bool(getenv("COLLECT_STATIC"))
SRC_DIR = dirname(dirname(abspath(__file__)))
PROJECT_DIR = dirname(SRC_DIR)
PROJECT_DOMAIN = getenv("PROJECT_DOMAIN")
REDIS_URL = getenv("REDIS_URL")

# Debug
DEBUG = bool(getenv("DEBUG"))
INTERNAL_IPS = [getenv("INTERNAL_IP")]

ADMIN_EMAIL = getenv("ADMIN_EMAIL")
SECRET_KEY = getenv("SECRET_KEY")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "githubcontrib",
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WSGI_APPLICATION = "githubcontrib_project.wsgi.application"
ROOT_URLCONF = "githubcontrib_project.urls"
SESSION_SAVE_EVERY_REQUEST = True

ALLOWED_HOSTS = [PROJECT_DOMAIN]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Custom
    "admin_reorder",
    "rosetta",
    "social_django",
    "menu",
    "githubcontrib",
]
if DEBUG:  # pragma: no cover
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

if not DEBUG:  # pragma: no cover
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

if IS_DEV or COLLECT_STATIC:  # pragma: no cover
    INSTALLED_APPS.append("django.contrib.staticfiles")

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom
    "django.middleware.gzip.GZipMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "githubcontrib.middleware.AjaxHandlerMiddleware",
    "githubcontrib.middleware.language_middleware",
]
if DEBUG:  # pragma: no cover
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

TEMPLATES: list[TemplatesSettings] = [
    {
        "NAME": "Main",
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [join(SRC_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                # social_django
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                # githubcontrib
                "githubcontrib.context_processors.variables",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
            "builtins": ["django.templatetags.static", "django.templatetags.i18n"],
        },
    }
]
if IS_DEV:  # pragma: no cover
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    ]

# Static files
if IS_DEV:  # pragma: no cover
    STATICFILES_DIRS = (join(SRC_DIR, "githubcontrib", "static"),)
    STATIC_ROOT = None
else:
    STATIC_ROOT = join(PROJECT_DIR, "static")

STATIC_URL = getenv("STATIC_URL", "/static/")

# Media files
MEDIA_ROOT = join(PROJECT_DIR, "media")
MEDIA_URL = "/media/"

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f"https://{PROJECT_DOMAIN}"]

# Authentification
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "githubcontrib.User"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # Custom
    "social_core.backends.github.GithubOAuth2",
)

# Internationalization
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", "English"),
    ("ru", "Русский"),
)
LOCALE_PATHS = (join(SRC_DIR, "locale"),)

# Timezone
TIME_ZONE = "US/Eastern"
USE_TZ = True

# Login
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

# --== Modules settings ==--

# django-modeladmin-reorder
ADMIN_REORDER = (
    {
        "app": "githubcontrib",
        "models": ("githubcontrib.User", "githubcontrib.Repo", "githubcontrib.Commit"),
    },
    {"app": "social_django", "models": ("social_django.UserSocialAuth",)},
)

# django-debug-toolbar
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# social-auth-app-django

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    "social_core.pipeline.social_auth.social_details",
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    "social_core.pipeline.social_auth.social_uid",
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    "social_core.pipeline.social_auth.auth_allowed",
    # Checks if the current social-account is already associated in the site.
    "social_core.pipeline.social_auth.social_user",
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    "social_core.pipeline.user.get_username",
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',
    # Create a user account if we haven't found one yet.
    "social_core.pipeline.user.create_user",
    # Create the record that associates the social account with the user.
    "social_core.pipeline.social_auth.associate_user",
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    "social_core.pipeline.social_auth.load_extra_data",
    # We might want to enable it
    # # Update the user record with any changed info from the auth service.
    # 'social_core.pipeline.user.user_details',
    # Custom
    # We do this only if the user get's created for the first time.
    "githubcontrib.social.load_user_data",
)
SOCIAL_AUTH_GITHUB_KEY = getenv("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = getenv("SOCIAL_AUTH_GITHUB_SECRET")

# --== Project settings ==--

# API Keys
GITHUB_API_KEY = getenv("GITHUB_API_KEY")

GOOGLE_ANALYTICS_ID = getenv("GOOGLE_ANALYTICS_ID")
