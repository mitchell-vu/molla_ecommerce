from .models import Cart, CartItem
from .views import _cart_id


def cart_preview(request):
    if 'admin' in request.path:
        return {}
    else:
        current_user = request.user
        try:
            if current_user.is_authenticated:
                cart = Cart.objects.get(user=current_user)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))
                
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = sum([cart_item.quantity for cart_item in cart_items])
        except Cart.DoesNotExist:
            cart_count = 0
            cart_items = {}
    return dict(
        sub_total=cart.sub_total,
        cart_items=cart_items,
        cart_count=cart_count,
    )
