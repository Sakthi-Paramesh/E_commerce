from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/buy-now/', views.buy_now, name='buy_now'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/to-cart/', views.wishlist_to_cart, name='wishlist_to_cart'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('order/success/<str:order_number>/', views.order_success, name='order_success'),
]
