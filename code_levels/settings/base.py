import os
from pathlib import Path
from dotenv import load_dotenv

from code_levels.settings.allauth.base import *
from code_levels.settings.plugins.colored_logs import *
from code_levels.settings.admin.jazzmin import JAZZMIN_SETTINGS_DICT
from code_levels.settings.drf import REST_FRAMEWORK, SIMPLE_JWT

from code_levels.settings.config.Dotenv import dotenv

# plugins
from code_levels.settings.plugins.summernote import SUMMERNOTE_THEME, SUMMERNOTE_CONFIG


load_dotenv(".env")


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = dotenv.django_secret_key
ALLOWED_HOSTS = dotenv.allowed_hosts.split(",")


JAZZMIN_SETTINGS = JAZZMIN_SETTINGS_DICT


INSTALLED_APPS = [
    "modeltranslation",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # third-party
    "rest_framework",
    # auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # apps
    "api.apps.ApiConfig",
    "platform_web.apps.PlatformWebConfig",
    "nested_admin",
    "adminsortable2",
    "django_summernote",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middleware
    "platform_web.middleware.PreferredLanguageMiddleware",
    "platform_web.middleware.AdminStaffOnlyMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "code_levels.urls"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "platform_web" / "templates",
            BASE_DIR / "platform_web" / "templates" / "account",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # ? custom context processors
                "platform_web.context_processors.website_config",
            ],
        },
    },
]

WSGI_APPLICATION = "code_levels.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": dotenv.pgdatabase,
        "USER": dotenv.pguser,
        "PASSWORD": dotenv.pgpassword,
        "HOST": dotenv.pghost,
        "PORT": dotenv.pgport,
    }
}


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


# i18n
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
