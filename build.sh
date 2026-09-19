#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# If RESET_DB=1 is set, flush all data and reload fixtures (run ONCE then remove the env var)
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
