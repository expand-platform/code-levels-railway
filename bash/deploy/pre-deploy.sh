#!/usr/bin/env bash
set -e

echo "Starting pre-deploy script..."

echo "Ensuring staticfiles directory exists..."
mkdir -p staticfiles

echo "Running system checks..."
python manage.py check --deploy --settings=code_levels.settings.prod

echo "Applying migrations..."
python manage.py migrate --noinput --settings=code_levels.settings.prod

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=code_levels.settings.prod