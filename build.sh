#!/usr/bin/env bash
# Render build script — runs on every deploy.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the admin account on first deploy, if the env vars are set.
# createsuperuser --noinput reads DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD.
# If the user already exists it exits non-zero, which we swallow so the
# build never fails on later deploys.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput || true
fi
