import logging

# Custom filter for coloring HTTP status codes
class StatusCodeColorFilter(logging.Filter):
    def filter(self, record):
        record.log_color = ''
        if hasattr(record, 'status_code'):
            code = record.status_code
            if 200 <= code < 300:
                record.log_color = '\033[92m'  # Green
            elif 300 <= code < 400:
                record.log_color = '\033[93m'  # Yellow
            elif 400 <= code < 600:
                record.log_color = '\033[91m'  # Red
        else:
            msg = record.getMessage()
            if ' 404 ' in msg or msg.endswith(' 404'):
                record.log_color = '\033[91m'  # Red
            elif ' 500 ' in msg or msg.endswith(' 500'):
                record.log_color = '\033[91m'  # Red
            elif ' 3' in msg:
                record.log_color = '\033[93m'  # Yellow
        return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "status_code_color": {
            "()": StatusCodeColorFilter,
        },
    },
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(message)s\033[0m",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "color",
            "filters": ["status_code_color"],
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}