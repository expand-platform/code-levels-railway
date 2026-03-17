import os
from code_levels.settings.base import *
from code_levels.settings.allauth.prod import *

from code_levels.settings.config.Dotenv import dotenv

DEBUG = False

INSTALLED_APPS += [
    "storages",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CSRF_TRUSTED_ORIGINS = dotenv.csrf_trusted_origins.split(",")

AWS_ACCESS_KEY_ID = dotenv.aws_access_key_id
AWS_SECRET_ACCESS_KEY = dotenv.aws_secret_access_key
AWS_STORAGE_BUCKET_NAME = dotenv.aws_storage_bucket_name
AWS_S3_ENDPOINT_URL = dotenv.aws_s3_endpoint_url

AWS_S3_CUSTOM_DOMAIN = "pub-4ca7ec1159154d25b3558c36ee3d304d.r2.dev"


AWS_QUERYSTRING_AUTH = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "location": "",  
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {},
    },
}



CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in dotenv.csrf_trusted_origins.split(",")
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
