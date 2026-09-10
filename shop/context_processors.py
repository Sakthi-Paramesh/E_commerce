from .models import Cart, Wishlist


def cart_wishlist_processor(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0

        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist.items.count()
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }
