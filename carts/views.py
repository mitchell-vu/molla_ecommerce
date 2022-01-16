from django.shortcuts import render, redirect, get_object_or_404
from .models import *

import json
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


# Tạo 1 id giỏ hàng trong session_storage nếu đây là lần đầu truy cập của máy local
# Nếu tồn tại id trong session_storage rồi thì chỉ cần lấy ra
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))

    return cart


# Cart view
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = get_cart(request)

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
        total = cart.sub_total()
        grand_total = total
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }

    return render(request, 'carts/cart.html', context)


# Sau khi dùng hàm _cart_id để chắc chắn là tồn tại 1 Cart ở máy local
# Hàm này tiến hành thêm mới 1 CartItem nếu chưa có CartItem trong Cart,
# Hoặc thêm 1 đơn vị số lượng vào CartItem đã tồn tại
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    quantity = request.POST.get('quantity') or json.loads(request.body)['quantity']

    print(product, quantity)
    # Get Variantions
    product_variations = list()
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__category_name__iexact=key,
                    variation_value__iexact=value
                )
                product_variations.append(variation)
            except ObjectDoesNotExist:
                pass
    else:
        return redirect('cart')

    # Get Cart
    if current_user.is_authenticated:
        cart, cartCreated = Cart.objects.get_or_create(user=current_user)
        cart_items = CartItem.objects.filter(product=product, cart=cart)
    else:
        try:
            # Get cart using the _cart_id
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

    # Check for the CartItem
    if cart_items.exists():
        existing_variation_list = [
            list(item.variations.all()) for item in cart_items]
        id = [item.id for item in cart_items]

        if product_variations in existing_variation_list:
            index = existing_variation_list.index(product_variations)
            cart_item = CartItem.objects.get(id=id[index])
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=quantity
            )
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=quantity
        )

    # Add variations to the cart item
    if len(product_variations) > 0:
        cart_item.variations.clear()
        for item in product_variations:
            cart_item.variations.add(item)
    cart_item.save()

    return redirect('cart')


# Giảm 1 đơn vị số lượng trong CartItem
def remove_cart(request, cart_item_id):
    try:
        cart = get_cart(request)
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            cart=cart
        )
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        pass

    return redirect('cart')


# Xóa hẳn 1 CartItem trong Cart
def remove_cart_item(request, cart_item_id):
    try:
        cart = get_cart(request)
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            cart=cart
        )
        cart_item.delete()
    except Exception:
        pass

    return redirect(request.META['HTTP_REFERER'])


def checkout(request):
    context = {

    }

    return render(request, 'carts/checkout.html', context)