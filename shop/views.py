from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import json

from .models import (Category, Brand, Product, ProductImage,
                     Review, Cart, CartItem, Wishlist, WishlistItem,
                     Order, OrderItem)
from .forms import ReviewForm, CheckoutForm, ProductSearchForm


# ─────────────────────────────────────────────
#  Helper: get or create cart for session/user
# ─────────────────────────────────────────────
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart


def merge_cart_on_login(request, user):
    """Merge anonymous session cart into the user's cart after login."""
    session_key = request.session.session_key
    if session_key:
        try:
            anon_cart = Cart.objects.get(session_key=session_key, user=None)
            user_cart, _ = Cart.objects.get_or_create(user=user)
            for item in anon_cart.items.all():
                existing = user_cart.items.filter(product=item.product).first()
                if existing:
                    existing.quantity += item.quantity
                    existing.save()
                else:
                    item.cart = user_cart
                    item.save()
            anon_cart.delete()
        except Cart.DoesNotExist:
            pass


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
def home(request):
    categories = Category.objects.filter(is_active=True)[:10]
    featured_products = Product.objects.filter(is_active=True, is_featured=True).prefetch_related('images')[:8]
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True).prefetch_related('images')[:8]
    best_sellers = Product.objects.filter(is_active=True).order_by('-sold_count').prefetch_related('images')[:8]
    reviews = Review.objects.select_related('user', 'product').order_by('-created_at')[:6]

    static_testimonials = [
        {'name': 'Rahul Sharma', 'initials': 'RS', 'review': 'Great product quality and super fast delivery! Highly recommend ShopWave!'},
        {'name': 'Priya Nair', 'initials': 'PN', 'review': 'Amazing experience shopping here. The variety is incredible and prices are unbeatable.'},
        {'name': 'Ankit Verma', 'initials': 'AV', 'review': 'Excellent customer service. Returned an item effortlessly. Will definitely shop again!'},
        {'name': 'Sneha Iyer', 'initials': 'SI', 'review': 'Love the website — easy to use and the products are exactly as described.'},
        {'name': 'Karan Mehta', 'initials': 'KM', 'review': 'Got my laptop in 2 days. ShopWave is my go-to for electronics now!'},
        {'name': 'Divya Rao', 'initials': 'DR', 'review': 'Beautiful collection of clothes. The quality is top-notch and prices are fair.'},
    ]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'reviews': reviews,
        'testimonials_static': static_testimonials,
    }
    return render(request, 'home.html', context)


# ─────────────────────────────────────────────
#  SHOP
# ─────────────────────────────────────────────
def shop(request):
    products = Product.objects.filter(is_active=True).prefetch_related('images').select_related('category', 'brand')
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    # Filters
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('rating')
    sort_by = request.GET.get('sort', 'latest')
    q = request.GET.get('q', '')

    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            products = products.filter(category=selected_category)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if min_rating:
        products = products.filter(rating__gte=min_rating)

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q) |
            Q(category__name__icontains=q) | Q(brand__name__icontains=q)
        )

    # Sorting
    sort_options = {
        'latest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'popular': '-sold_count',
        'rating': '-rating',
    }
    products = products.order_by(sort_options.get(sort_by, '-created_at'))

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Wishlist product IDs for current user
    wishlist_product_ids = []
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))
        except Wishlist.DoesNotExist:
            pass

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': brand_slug,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'sort_by': sort_by,
        'q': q,
        'total_products': products.count() if hasattr(products, 'count') else paginator.count,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'shop/shop.html', context)


# ─────────────────────────────────────────────
#  PRODUCT DETAIL
# ─────────────────────────────────────────────
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.select_related('user').all()
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).prefetch_related('images')[:4]

    # Review form
    review_form = ReviewForm()
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            if user_review:
                messages.warning(request, 'You have already reviewed this product.')
            else:
                r = review_form.save(commit=False)
                r.product = product
                r.user = request.user
                r.save()
                # Update product rating
                avg = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
                product.rating = round(avg, 1)
                product.review_count = product.reviews.count()
                product.save(update_fields=['rating', 'review_count'])
                messages.success(request, 'Review submitted successfully!')
                return redirect('product_detail', slug=slug)

    # Wishlist check
    in_wishlist = False
    if request.user.is_authenticated:
        try:
            wl = Wishlist.objects.get(user=request.user)
            in_wishlist = wl.items.filter(product=product).exists()
        except Wishlist.DoesNotExist:
            pass

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'rating_range': range(1, 6),
    }
    return render(request, 'shop/product_detail.html', context)


# ─────────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────────
def search(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q) |
            Q(category__name__icontains=q) | Q(brand__name__icontains=q)
        ).filter(is_active=True).prefetch_related('images').select_related('category', 'brand')

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'q': q,
        'page_obj': page_obj,
        'total': paginator.count,
    }
    return render(request, 'shop/search_results.html', context)


# ─────────────────────────────────────────────
#  CART
# ─────────────────────────────────────────────
def cart_view(request):
    cart = get_or_create_cart(request)

    # Handle clear cart action
    if request.GET.get('clear') == '1':
        cart.items.all().delete()
        messages.success(request, 'Your cart has been cleared.')
        return redirect('cart')

    items = cart.items.select_related('product').prefetch_related('product__images').all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)


@require_POST
def add_to_cart(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if not product.is_in_stock:
        return JsonResponse({'success': False, 'message': 'Product is out of stock.'})

    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.quantity = min(item.quantity, product.stock)
    item.save()

    return JsonResponse({
        'success': True,
        'message': f'"{product.name}" added to cart!',
        'cart_count': cart.total_items,
    })


@require_POST
def update_cart(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))

    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    if quantity <= 0:
        item_total = '0'
        item.delete()
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()
        item_total = str(item.total_price)

    return JsonResponse({
        'success': True,
        'cart_count': cart.total_items,
        'item_total': item_total,
        'subtotal': str(cart.subtotal),
        'shipping': str(cart.shipping),
        'tax': str(cart.tax),
        'grand_total': str(cart.grand_total),
    })


@require_POST
def remove_from_cart(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    item_id = data.get('item_id')
    cart = get_or_create_cart(request)
    CartItem.objects.filter(pk=item_id, cart=cart).delete()
    return JsonResponse({'success': True, 'cart_count': cart.total_items})


# ─────────────────────────────────────────────
#  BUY NOW — cart-க்கு add செய்து checkout-க்கு redirect
# ─────────────────────────────────────────────
@require_POST
def buy_now(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if not product.is_in_stock:
        return JsonResponse({'success': False, 'message': 'Product is out of stock.'})

    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.quantity = min(item.quantity, product.stock)
    item.save()

    return JsonResponse({'success': True, 'redirect': '/checkout/'})


# ─────────────────────────────────────────────
#  WISHLIST
# ─────────────────────────────────────────────
@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product').prefetch_related('product__images').all()
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist, 'items': items})


@login_required
@require_POST
def toggle_wishlist(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    item = wishlist.items.filter(product=product).first()
    if item:
        item.delete()
        added = False
        msg = f'"{product.name}" removed from wishlist.'
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        added = True
        msg = f'"{product.name}" added to wishlist!'
    return JsonResponse({
        'success': True,
        'added': added,
        'message': msg,
        'wishlist_count': wishlist.items.count(),
    })


@login_required
@require_POST
def wishlist_to_cart(request):
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.items.filter(product=product).delete()
    return JsonResponse({
        'success': True,
        'message': f'"{product.name}" moved to cart!',
        'cart_count': cart.total_items,
        'wishlist_count': wishlist.items.count(),
    })


# ─────────────────────────────────────────────
#  CHECKOUT
# ─────────────────────────────────────────────
@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    if not items.exists():
        messages.warning(request, 'Your cart is empty. Add products before checkout.')
        return redirect('cart')

    # Pre-fill from default address or user data
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    default_address = user.addresses.filter(is_default=True).first()
    initial_data = {
        'full_name': f"{user.first_name} {user.last_name}".strip(),
        'email': user.email,
        'phone': profile.phone if profile else '',
    }
    if default_address:
        initial_data.update({
            'address_line1': default_address.address_line1,
            'city': default_address.city,
            'state': default_address.state,
            'pincode': default_address.pincode,
            'country': default_address.country,
        })

    form = CheckoutForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        order = Order.objects.create(
            user=user,
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            address_line1=data['address_line1'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode'],
            country=data['country'],
            payment_method=data['payment_method'],
            notes=data.get('notes', ''),
            subtotal=cart.subtotal,
            discount=cart.discount_total,
            shipping_charge=cart.shipping,
            tax=cart.tax,
            total=cart.grand_total,
        )
        # Create order items and reduce stock
        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.effective_price,
                quantity=cart_item.quantity,
            )
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.sold_count += cart_item.quantity
            cart_item.product.save(update_fields=['stock', 'sold_count'])

        cart.items.all().delete()
        messages.success(request, 'Order placed successfully! 🎉')
        return redirect('order_success', order_number=order.order_number)

    context = {
        'form': form,
        'cart': cart,
        'items': items,
        'addresses': user.addresses.all(),
    }
    return render(request, 'shop/checkout.html', context)


# ─────────────────────────────────────────────
#  ORDERS
# ─────────────────────────────────────────────
@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'shop/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    items = order.items.select_related('product').all()
    return render(request, 'shop/order_detail.html', {'order': order, 'items': items})


# ─────────────────────────────────────────────
#  CATEGORY PAGE
# ─────────────────────────────────────────────
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return redirect(f'/shop/?category={slug}')
