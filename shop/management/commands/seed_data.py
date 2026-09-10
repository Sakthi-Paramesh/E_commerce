"""
Management command: python manage.py seed_data
Populates the database with demo categories, brands, and products.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Brand, Product, Review
from accounts.models import Profile
import random


class Command(BaseCommand):
    help = 'Seed the database with demo categories, brands, and products'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()

        self.stdout.write('Seeding categories...')
        categories_data = [
            {'name': 'Electronics', 'icon': 'bi bi-phone', 'description': 'Latest gadgets and electronics'},
            {'name': 'Fashion', 'icon': 'bi bi-bag', 'description': 'Trendy clothing and accessories'},
            {'name': 'Men\'s Fashion', 'icon': 'bi bi-person', 'description': 'Clothing for men'},
            {'name': 'Women\'s Fashion', 'icon': 'fa-solid fa-person-dress', 'description': 'Clothing for women'},
            {'name': 'Shoes', 'icon': 'fa-solid fa-shoe-prints', 'description': 'Footwear for all occasions'},
            {'name': 'Beauty', 'icon': 'bi bi-stars', 'description': 'Skincare, makeup and beauty products'},
            {'name': 'Home & Kitchen', 'icon': 'bi bi-house-heart', 'description': 'Home appliances and decor'},
            {'name': 'Sports', 'icon': 'bi bi-trophy', 'description': 'Sports and fitness equipment'},
            {'name': 'Gadgets', 'icon': 'bi bi-cpu', 'description': 'Smart gadgets and accessories'},
            {'name': 'Accessories', 'icon': 'bi bi-watch', 'description': 'Watches, bags and accessories'},
        ]
        categories = {}
        for data in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=data['name'],
                defaults={'icon': data['icon'], 'description': data['description']}
            )
            categories[data['name']] = cat
            self.stdout.write(f'  [OK] Category: {cat.name}')

        self.stdout.write('Seeding brands...')
        brands_data = ['Apple', 'Samsung', 'Sony', 'Nike', 'Adidas', 'Puma',
                       'H&M', 'Zara', 'LOreal', 'Lakme', 'Philips', 'boAt',
                       'OnePlus', 'Realme', 'Xiaomi', 'Titan', 'Fastrack']
        brands = {}
        for name in brands_data:
            from django.utils.text import slugify
            slug = slugify(name)
            brand, _ = Brand.objects.get_or_create(slug=slug, defaults={'name': name})
            brands[name] = brand
            self.stdout.write(f'  [OK] Brand: {brand.name}')

        self.stdout.write('Seeding products...')

        # High-quality Unsplash product images
        electronics_imgs = [
            'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&q=80',
            'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&q=80',
            'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&q=80',
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',
            'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80',
        ]
        fashion_imgs = [
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&q=80',
            'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600&q=80',
            'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&q=80',
            'https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600&q=80',
        ]
        shoe_imgs = [
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
            'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&q=80',
            'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=600&q=80',
        ]
        beauty_imgs = [
            'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80',
            'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&q=80',
        ]
        sports_imgs = [
            'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80',
            'https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&q=80',
        ]
        home_imgs = [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
            'https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&q=80',
        ]

        products_data = [
            # Electronics
            {'name': 'iPhone 15 Pro Max', 'category': 'Electronics', 'brand': 'Apple',
             'price': 134900, 'discount_price': 119900, 'stock': 25, 'rating': 4.8,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'The most powerful iPhone ever. Features the A17 Pro chip, titanium design, and a 48MP main camera system.',
             'specifications': 'Chip: A17 Pro\nStorage: 256GB\nDisplay: 6.7" Super Retina XDR\nCamera: 48MP Main\nBattery: 4422mAh',
             'img_url': electronics_imgs[0]},
            {'name': 'Samsung Galaxy S24 Ultra', 'category': 'Electronics', 'brand': 'Samsung',
             'price': 124999, 'discount_price': 109999, 'stock': 30, 'rating': 4.7,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'Next level Galaxy AI with Galaxy S24 Ultra. Features a 200MP camera, S Pen, and titanium frame.',
             'specifications': 'Chip: Snapdragon 8 Gen 3\nStorage: 256GB\nDisplay: 6.8" AMOLED\nCamera: 200MP',
             'img_url': electronics_imgs[0]},
            {'name': 'Sony WH-1000XM5 Headphones', 'category': 'Electronics', 'brand': 'Sony',
             'price': 29990, 'discount_price': 24990, 'stock': 50, 'rating': 4.9,
             'is_featured': True,
             'description': 'Industry-leading noise canceling with exceptional sound quality. 30-hour battery life.',
             'specifications': 'Type: Over-ear\nBattery: 30 hours\nDriver: 30mm\nBluetooth: 5.2',
             'img_url': electronics_imgs[1]},
            {'name': 'Apple MacBook Air M3', 'category': 'Electronics', 'brand': 'Apple',
             'price': 114900, 'discount_price': 104900, 'stock': 15, 'rating': 4.9,
             'is_featured': True,
             'description': 'Supercharged by the M3 chip. Blazing-fast performance in an ultra-thin design.',
             'specifications': 'Chip: Apple M3\nRAM: 8GB\nStorage: 256GB SSD\nDisplay: 13.6" Liquid Retina',
             'img_url': electronics_imgs[4]},
            {'name': 'boAt Rockerz 450 Pro', 'category': 'Electronics', 'brand': 'boAt',
             'price': 2499, 'discount_price': 1299, 'stock': 200, 'rating': 4.2,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'Wireless Bluetooth headphones with 70 hours playback, deep bass and foldable design.',
             'specifications': 'Battery: 70 hours\nDriver: 40mm\nBluetooth: 5.0',
             'img_url': electronics_imgs[1]},
            {'name': 'OnePlus 12 5G', 'category': 'Electronics', 'brand': 'OnePlus',
             'price': 64999, 'discount_price': 57999, 'stock': 40, 'rating': 4.6,
             'is_featured': True,
             'description': 'Flagship performance with Snapdragon 8 Gen 3, 50W wireless charging, and Hasselblad cameras.',
             'specifications': 'Chip: Snapdragon 8 Gen 3\nStorage: 256GB\nDisplay: 6.82" AMOLED\nCharging: 100W',
             'img_url': electronics_imgs[0]},

            # Fashion
            {'name': 'Nike Air Max 270', 'category': 'Shoes', 'brand': 'Nike',
             'price': 11995, 'discount_price': 8995, 'stock': 75, 'rating': 4.5,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'The Nike Air Max 270 delivers a big, bold look with an ultra-comfortable Air unit.',
             'img_url': shoe_imgs[1]},
            {'name': 'Adidas Ultraboost 23', 'category': 'Shoes', 'brand': 'Adidas',
             'price': 17999, 'discount_price': 13999, 'stock': 60, 'rating': 4.7,
             'is_featured': True,
             'description': 'Experience incredible energy return and comfort with Boost technology.',
             'img_url': shoe_imgs[2]},
            {'name': 'Puma Men\'s Polo T-Shirt', 'category': 'Men\'s Fashion', 'brand': 'Puma',
             'price': 2499, 'discount_price': 1499, 'stock': 150, 'rating': 4.3,
             'is_new_arrival': True,
             'description': 'Classic polo t-shirt with moisture-wicking fabric for all-day comfort.',
             'img_url': fashion_imgs[2]},
            {'name': 'Zara Women\'s Floral Dress', 'category': 'Women\'s Fashion', 'brand': 'Zara',
             'price': 3999, 'discount_price': 2499, 'stock': 80, 'rating': 4.4,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'Elegant floral print dress perfect for casual and semi-formal occasions.',
             'img_url': fashion_imgs[4]},
            {'name': 'H&M Slim Fit Jeans', 'category': 'Men\'s Fashion', 'brand': 'H&M',
             'price': 2999, 'discount_price': 1799, 'stock': 120, 'rating': 4.1,
             'is_new_arrival': True,
             'description': 'Modern slim fit jeans with stretch fabric for maximum comfort.',
             'img_url': fashion_imgs[0]},
            {'name': 'Titan Raga Women\'s Watch', 'category': 'Accessories', 'brand': 'Titan',
             'price': 8995, 'discount_price': 6995, 'stock': 45, 'rating': 4.6,
             'is_featured': True,
             'description': 'Elegant women\'s watch with rose gold plating and leather strap.',
             'img_url': electronics_imgs[3]},
            {'name': 'Fastrack Casual Watch', 'category': 'Accessories', 'brand': 'Fastrack',
             'price': 2995, 'discount_price': 1995, 'stock': 90, 'rating': 4.2,
             'is_new_arrival': True,
             'description': 'Stylish casual watch with silicon strap and water-resistant design.',
             'img_url': electronics_imgs[3]},

            # Beauty
            {'name': 'LOreal Revitalift Face Cream', 'category': 'Beauty', 'brand': 'LOreal',
             'price': 899, 'discount_price': 649, 'stock': 200, 'rating': 4.4,
             'is_featured': True,
             'description': 'Anti-aging face cream with Pro-Retinol and Centella. Visibly reduces wrinkles.',
             'img_url': beauty_imgs[0]},
            {'name': 'Lakme Absolute Lipstick', 'category': 'Beauty', 'brand': 'Lakme',
             'price': 699, 'discount_price': 499, 'stock': 300, 'rating': 4.3,
             'is_new_arrival': True,
             'description': 'Long-lasting matte lipstick in 30+ shades. Up to 12 hours wear.',
             'img_url': beauty_imgs[1]},

            # Sports
            {'name': 'Adidas Yoga Mat Pro', 'category': 'Sports', 'brand': 'Adidas',
             'price': 3999, 'discount_price': 2499, 'stock': 100, 'rating': 4.5,
             'is_featured': True,
             'description': 'Premium non-slip yoga mat with alignment lines and carrying strap.',
             'img_url': sports_imgs[0]},
            {'name': 'Nike Dri-FIT Training Shorts', 'category': 'Sports', 'brand': 'Nike',
             'price': 2499, 'discount_price': 1799, 'stock': 130, 'rating': 4.4,
             'is_new_arrival': True,
             'description': 'Lightweight training shorts with sweat-wicking Dri-FIT technology.',
             'img_url': sports_imgs[1]},

            # Home & Kitchen
            {'name': 'Philips Air Fryer HD9252', 'category': 'Home & Kitchen', 'brand': 'Philips',
             'price': 9999, 'discount_price': 6999, 'stock': 35, 'rating': 4.6,
             'is_featured': True,
             'description': 'Rapid Air Technology air fryer. Fry, bake, grill with little to no oil.',
             'img_url': home_imgs[0]},
            {'name': 'Prestige Induction Cooktop', 'category': 'Home & Kitchen', 'brand': 'Philips',
             'price': 3499, 'discount_price': 2299, 'stock': 55, 'rating': 4.3,
             'is_new_arrival': True,
             'description': 'Energy-efficient 2000W induction cooktop with 8 power levels.',
             'img_url': home_imgs[1]},

            # Gadgets
            {'name': 'Sony PlayStation 5', 'category': 'Gadgets', 'brand': 'Sony',
             'price': 54990, 'discount_price': 49990, 'stock': 10, 'rating': 4.9,
             'is_featured': True,
             'description': 'Next-gen gaming with lightning-fast SSD, 3D audio, and DualSense controller.',
             'specifications': 'CPU: AMD Zen 2\nGPU: 10.28 TFLOPS\nStorage: 825GB SSD',
             'img_url': electronics_imgs[2]},
            {'name': 'Apple iPad Air (2024)', 'category': 'Gadgets', 'brand': 'Apple',
             'price': 59900, 'discount_price': 54900, 'stock': 20, 'rating': 4.8,
             'is_featured': True, 'is_new_arrival': True,
             'description': 'Powerful. Colorful. Wonderful. M2 chip for superfast performance.',
             'img_url': electronics_imgs[4]},
        ]

        for p_data in products_data:
            img_url = p_data.pop('img_url', None)
            p_data.setdefault('review_count', random.randint(5, 200))
            p_data.setdefault('sold_count', random.randint(10, 500))
            p_data.setdefault('is_featured', False)
            p_data.setdefault('is_new_arrival', False)
            p_data.setdefault('specifications', '')

            cat_name = p_data.pop('category')
            brand_name = p_data.pop('brand')

            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    **p_data,
                    'category': categories.get(cat_name, list(categories.values())[0]),
                    'brand': brands.get(brand_name),
                }
            )
            if created:
                self.stdout.write(f'  [OK] Product: {product.name}')
            else:
                self.stdout.write(f'  [EXISTS] {product.name}')

        # Create a demo superuser
        if not User.objects.filter(username='admin@shopwave.com').exists():
            admin = User.objects.create_superuser(
                username='admin@shopwave.com',
                email='admin@shopwave.com',
                password='admin123',
                first_name='Admin',
                last_name='ShopWave',
            )
            Profile.objects.get_or_create(user=admin)
            self.stdout.write(self.style.SUCCESS('  [OK] Admin user: admin@shopwave.com / admin123'))

        # Create a demo regular user
        if not User.objects.filter(username='demo@shopwave.com').exists():
            demo = User.objects.create_user(
                username='demo@shopwave.com',
                email='demo@shopwave.com',
                password='demo123',
                first_name='Priya',
                last_name='Sharma',
            )
            Profile.objects.get_or_create(user=demo, defaults={'phone': '9876543210'})
            self.stdout.write(self.style.SUCCESS('  [OK] Demo user: demo@shopwave.com / demo123'))

        self.stdout.write(self.style.SUCCESS(
            f'\nSEEDING COMPLETE!\n'
            f'   Categories: {Category.objects.count()}\n'
            f'   Brands: {Brand.objects.count()}\n'
            f'   Products: {Product.objects.count()}\n\n'
            f'   Admin: admin@shopwave.com / admin123\n'
            f'   Demo:  demo@shopwave.com / demo123\n'
        ))
