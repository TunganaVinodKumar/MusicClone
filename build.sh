#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# 3. Run database migrations on PostgreSQL
python manage.py migrate

# 4. Automatically load your exact admin accounts, songs, and playlists
python manage.py loaddata data.json || true
