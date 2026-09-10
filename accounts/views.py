from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, AddressForm, CustomPasswordChangeForm
from .models import Profile, Address
from shop.views import merge_cart_on_login


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        merge_cart_on_login(request, user)
        messages.success(request, f'Welcome to ShopWave, {user.first_name}! 🎉')
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            merge_cart_on_login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    orders = user.orders.order_by('-created_at')[:5]
    addresses = user.addresses.all()

    context = {
        'profile': profile,
        'orders': orders,
        'addresses': addresses,
        'active_tab': request.GET.get('tab', 'overview'),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile, user=user)
    if request.method == 'POST' and form.is_valid():
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['email']
        user.save()
        form.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully!')
        return redirect('profile')
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def add_address(request):
    form = AddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, 'Address added successfully!')
        return redirect('profile')
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add Address'})


@login_required
def edit_address(request, pk):
    address = Address.objects.get(pk=pk, user=request.user)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Address updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required
def delete_address(request, pk):
    Address.objects.filter(pk=pk, user=request.user).delete()
    messages.success(request, 'Address deleted.')
    return redirect('profile')
