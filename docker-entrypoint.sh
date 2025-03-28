#!/bin/bash
set -e

export VIRTUAL_ENV=/opt/venv

# # Set up migrations if needed
# echo "Setting up migrations..."
# python scripts/setup_migrations.py

# # Run migrations
# echo "Running migrations..."
# python scripts/run_migrations.py

# Start the application
echo "Starting web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
