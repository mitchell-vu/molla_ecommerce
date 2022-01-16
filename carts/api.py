from django.shortcuts import redirect
from .models import *

import json
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .views import _cart_id

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    quantity = json.loads(request.body)['quantity']

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
    
    return JsonResponse('Added', safe=False)


def update_cart(request):
    data = json.loads(request.body)
    for item in data:
        cart_item = CartItem.objects.get(id=data[item]['cart_item_id'])
        cart_item.quantity = data[item]['quantity']
        cart_item.save()

    return JsonResponse(data)
