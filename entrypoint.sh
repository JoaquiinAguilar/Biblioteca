#!/bin/bash
set -e

# --- Wait for database ---
echo "Waiting for PostgreSQL to be ready..."
# Simple sleep approach - wait for database to start
sleep 30
echo "PostgreSQL should be ready!"

# --- Fix ownership and permissions ---
# Ensure the appuser owns the application directory
chown -R appuser:appuser /app

# --- Django management commands ---
# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# --- Create superuser if needed (optional) ---
# Uncomment the following lines if you want to create a superuser automatically
# if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
#     echo "Creating superuser..."
#     python manage.py createsuperuser --noinput || true
# fi

# --- Switch to non-root user and start application ---
exec gunicorn --bind 0.0.0.0:8000 --workers 3 cubicle_project.wsgi:application