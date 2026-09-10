import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import Product, ProductImage

# Mapping of product slug to a good image URL
IMAGES = {
    'iphone-15-pro-max': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&q=80',
    'samsung-galaxy-s24-ultra': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&q=80',
    'sony-wh-1000xm5-headphones': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&q=80',
    'apple-macbook-air-m3': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80',
    'boat-rockerz-450-pro': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&q=80',
    'oneplus-12-5g': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&q=80',
    'nike-air-max-270': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
    'adidas-ultraboost-23': 'https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=600&q=80',
    'puma-mens-polo-t-shirt': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&q=80',
    'zara-womens-floral-dress': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&q=80',
    'hm-slim-fit-jeans': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&q=80',
    'titan-raga-womens-watch': 'https://images.unsplash.com/photo-1585123334904-845d60e97b29?w=600&q=80',
    'fastrack-casual-watch': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=600&q=80',
    'loreal-revitalift-face-cream': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&q=80',
    'lakme-absolute-lipstick': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=600&q=80',
    'adidas-yoga-mat-pro': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&q=80',
    'nike-dri-fit-training-shorts': 'https://images.unsplash.com/photo-1533681473523-28682b13cb09?w=600&q=80',
    'philips-air-fryer-hd9252': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&q=80',
    'prestige-induction-cooktop': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&q=80',
    'sony-playstation-5': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&q=80',
    'apple-ipad-air-2024': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&q=80',
}

def download_images():
    # Make sure media/products directory exists
    os.makedirs('media/products', exist_ok=True)
    
    products = Product.objects.all()
    for product in products:
        if product.images.exists():
            print(f"Skipping {product.name}, already has image.")
            continue
            
        url = IMAGES.get(product.slug)
        if not url:
            print(f"No URL mapping found for {product.slug}")
            continue
            
        print(f"Downloading image for {product.name}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
                
            img_name = f"{product.slug}.jpg"
            
            product_img = ProductImage(product=product, is_primary=True, alt_text=product.name)
            product_img.image.save(img_name, ContentFile(img_data), save=True)
            print(f"[OK] Successfully added image for {product.name}")
        except Exception as e:
            print(f"[FAIL] Failed to download for {product.name}: {e}")

if __name__ == '__main__':
    download_images()
