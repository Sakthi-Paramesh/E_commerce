from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, Review, Cart, CartItem, Order, OrderItem, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'get_product_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'is_primary', 'alt_text']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discount_price', 'stock',
                    'rating', 'is_featured', 'is_new_arrival', 'is_active', 'created_at']
    list_filter = ['category', 'brand', 'is_featured', 'is_new_arrival', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'discount_price', 'stock', 'is_featured', 'is_new_arrival', 'is_active']
    inlines = [ProductImageInline]
    readonly_fields = ['created_at', 'updated_at']

    def product_image(self, obj):
        if obj.primary_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />', obj.primary_image.image.url)
        return '-'
    product_image.short_description = 'Image'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified']
    search_fields = ['product__name', 'user__username', 'comment']
    list_editable = ['is_verified']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'total']
    fields = ['product', 'product_name', 'product_price', 'quantity']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'total', 'status',
                    'payment_method', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status']
    search_fields = ['order_number', 'user__username', 'full_name', 'email']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'total_items', 'created_at']
    list_filter = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
