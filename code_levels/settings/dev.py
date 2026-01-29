from code_levels.settings.base import *
from code_levels.settings.allauth.dev import *

DEBUG = True

INSTALLED_APPS += [
    "django_browser_reload",
]
MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]