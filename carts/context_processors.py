from .models import Cart, CartItem
from .views import get_cart, _cart_id


def cart_preview(request):
    if 'admin' in request.path:
        return {}
    else:
        current_user = request.user
        try:
            cart = get_cart(request)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = sum([cart_item.quantity for cart_item in cart_items])
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart_count = 0
            cart_items = {}
    return dict(
        sub_total=cart.sub_total,
        cart_items=cart_items,
        cart_count=cart_count,
    )
