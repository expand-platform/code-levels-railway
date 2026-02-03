import os
from code_levels.settings.base import *
from code_levels.settings.allauth.prod import *

DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {},
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {},
#     },
# }
# DEFAULT_FILE_STORAGE = STORAGES["default"]["BACKEND"]
# STATICFILES_STORAGE = STORAGES["staticfiles"]["BACKEND"]

AWS_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("R2_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("R2_ENDPOINT")

# media and static
# STATIC_URL = "static/"
MEDIA_URL = f"https://pub-4ca7ec1159154d25b3558c36ee3d304d.r2.dev/"

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
]


CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
