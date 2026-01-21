#!/bin/bash

# Script to create .env file with production settings from .env.prod
# This creates a new .env file for production deployment

echo "Creating .env file with production settings..."

cat > .env << 'EOF'
SECRET_KEY=SYfb49obs_gPwqGVcvooAcake8Bg1Au8Zdoe2NwQ8L-pu8O-uQ1WKyIhp-zDjLmMBTQ
DEBUG=False
ALLOWED_HOSTS=stanislavpy934.pythonanywhere.com,www.stanislavpy934.pythonanywhere.com

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/home/stanislavpy934/jobs-portal-django/db.sqlite3

DJANGO_SETTINGS_MODULE=jobs_portal.settings.prod
CSRF_TRUSTED_ORIGINS=https://stanislavpy934.pythonanywhere.com,http://stanislavpy934.pythonanywhere.co
EOF

echo "Done! .env file created with production settings."