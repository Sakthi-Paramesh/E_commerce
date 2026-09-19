"""
Management command helper to fix image paths in DB.
Run: python manage.py shell < fix_image_paths.py
Or directly: python fix_image_paths.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import ProductImage

fixed = 0
for img in ProductImage.objects.all():
    path = str(img.image)
    if path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        new_path = os.path.splitext(path)[0]
        img.image = new_path
        img.save()
        fixed += 1
        print(f"Fixed: {path} -> {new_path}")

print(f"\nTotal fixed: {fixed} image paths")
