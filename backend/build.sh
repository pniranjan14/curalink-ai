#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations to setup Supabase schema
python manage.py migrate

# Collect static files (if any)
python manage.py collectstatic --no-input
