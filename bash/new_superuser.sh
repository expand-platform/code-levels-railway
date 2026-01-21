#!/bin/bash

# ----------------------------
# Config - change these values
# ----------------------------
SUPERUSER_NAME="hero"
SUPERUSER_EMAIL="damir96.lukyanenko@gmail.com"
SUPERUSER_PASSWORD="super_hero_123"
# ----------------------------

echo "Creating Django superuser..."

# Export environment variables so Django can use them
export DJANGO_SUPERUSER_USERNAME=$SUPERUSER_NAME
export DJANGO_SUPERUSER_EMAIL=$SUPERUSER_EMAIL
export DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD

# Run Django command to create superuser
python manage.py createsuperuser --noinput

echo "Superuser '$SUPERUSER_NAME' created successfully!"
