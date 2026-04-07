#!/bin/sh
set -e

# Run database migrations
if [ -f manage.py ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput

  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

# Exec the container CMD
exec "$@"
