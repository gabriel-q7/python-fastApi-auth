#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Determine which server to use based on environment
if [ "$APP_ENV" = "production" ]; then
    echo "Starting Gunicorn with Uvicorn workers (Production mode)..."
    exec gunicorn app.main:app -c gunicorn.conf.py
else
    echo "Starting Uvicorn directly (Development mode)..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8008 --reload
fi
