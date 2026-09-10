# ShopWave — Premium E-Commerce Platform

A complete, modern, production-quality **Django E-Commerce Website** with Bootstrap 5, Poppins font, smooth animations, and full functionality.

## Features

- **Full Product Catalog** — Categories, brands, filtering, sorting, pagination
- **Search** — Full-text search across name, category, brand, description
- **Shopping Cart** — AJAX add/remove/update, real-time totals
- **Wishlist** — Heart toggle with AJAX
- **User Auth** — Register, login, logout with cart merge
- **User Profile** — Dashboard with orders, addresses, wishlist, edit profile
- **Checkout** — Multi-step with address selection, payment method
- **Orders** — Full order management with status timeline
- **Admin Panel** — Complete Django admin for products, orders, users
- **Responsive** — Mobile-first Bootstrap 5 design
- **Animations** — Scroll reveal, hover effects, toast notifications

## Quick Start

### 1. Install dependencies

```bash
pip install Django Pillow django-crispy-forms crispy-bootstrap5 python-decouple whitenoise
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Seed demo data

```bash
python manage.py seed_data
```

This creates:
- 10 categories, 17 brands, 21 products
- **Admin:** `admin@shopwave.com` / `admin123`
- **Demo User:** `demo@shopwave.com` / `demo123`

### 4. Run the development server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## Admin Panel

Visit: **http://127.0.0.1:8000/admin**  
Login: `admin@shopwave.com` / `admin123`

## Project Structure

```
e commerce/
├── manage.py
├── requirements.txt
├── ecommerce/              # Django project config
│   ├── settings.py
│   └── urls.py
├── shop/                   # Main app
│   ├── models.py           # Category, Product, Cart, Order, etc.
│   ├── views.py            # All shop views
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── context_processors.py
│   └── management/commands/seed_data.py
├── accounts/               # Auth app
│   ├── models.py           # Profile, Address
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── partials/product_card.html
│   ├── shop/               # shop, product_detail, cart, wishlist, etc.
│   └── accounts/           # login, register, profile, etc.
├── static/
│   ├── css/style.css
│   └── js/main.js
└── media/                  # Uploaded product images
```

## PostgreSQL (Production)

Create a `.env` file:

```
SECRET_KEY=your-production-secret-key
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=shopwave_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.x + Django 4.2 |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Font | Poppins (Google Fonts) |
| Icons | Bootstrap Icons + Font Awesome |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Images | Pillow |
| Auth | Django built-in |

## Pages

| URL | Page |
|-----|------|
| `/` | Home |
| `/shop/` | Shop with filters |
| `/product/<slug>/` | Product detail |
| `/search/?q=...` | Search results |
| `/cart/` | Shopping cart |
| `/wishlist/` | Wishlist |
| `/checkout/` | Checkout |
| `/orders/` | Order history |
| `/order/<id>/` | Order detail |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register |
| `/accounts/profile/` | Profile dashboard |
| `/admin/` | Django Admin |
