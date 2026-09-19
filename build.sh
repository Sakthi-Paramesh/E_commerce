#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Create/update Django admin user when credentials are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then

    echo ">>> Creating/updating Django admin user..."

    python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.environ['DJANGO_SUPERUSER_USERNAME']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True
    }
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

print('>>> Admin user created/updated successfully!')
"

fi

# If RESET_DB=1 is set, flush all data and reload fixtures
if [ "$RESET_DB" = "1" ]; then

    echo ">>> RESET_DB=1 detected: Flushing all data and reloading fixtures..."

    python manage.py flush --no-input

    python manage.py loaddata fixtures.json

    python fix_image_paths.py

    echo ">>> Database reset and fixture reload complete!"

else

    # Normal: Load initial product data only if no products exist

    python manage.py shell -c "from shop.models import Product; exit(0) if Product.objects.exists() else exit(1)" || (python manage.py loaddata fixtures.json && python fix_image_paths.py)

fi