from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['phone', 'avatar', 'bio', 'date_of_birth']


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'pincode', 'address_type', 'is_default']
    list_filter = ['address_type', 'is_default', 'country']
    search_fields = ['user__username', 'full_name', 'city']


# Customize Django admin site
admin.site.site_header = 'ShopWave Administration'
admin.site.site_title = 'ShopWave Admin'
admin.site.index_title = 'Welcome to ShopWave Admin Panel'
