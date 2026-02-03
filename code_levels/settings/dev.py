from code_levels.settings.base import *
from code_levels.settings.allauth.dev import *

DEBUG = True

MEDIA_URL = "/media/"

INSTALLED_APPS += [
    "django_browser_reload",
]
MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]