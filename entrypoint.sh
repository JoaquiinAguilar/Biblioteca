#!/bin/bash
set -e

# --- Configuration ---
# Read environment variables from .env file
if [ -f .env ]; then
    export $(grep -E '^POSTGRES_USER=|^POSTGRES_DB=' .env | xargs)
fi

# --- Wait for database ---
echo "Waiting for PostgreSQL to be ready..."
until python -c "import psycopg2; psycopg2.connect(host='$DATABASE_HOST', port='$DATABASE_PORT', user='$DATABASE_USER', password='$DATABASE_PASSWORD', dbname='$DATABASE_NAME')" 2>/dev/null; do
    sleep 2
done
echo "PostgreSQL is ready!"

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