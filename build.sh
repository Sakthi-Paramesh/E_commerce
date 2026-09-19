#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Load initial product data (only if no products exist)
python manage.py shell -c "from shop.models import Product; exit(0) if Product.objects.exists() else exit(1)" || python manage.py loaddata fixtures.json

# Fix image paths for Cloudinary (remove .jpg/.png extensions so Cloudinary serves them)
python fix_image_paths.py
