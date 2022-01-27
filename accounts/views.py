from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from accounts.models import Account, Wishlist
from orders.models import Order
from carts.views import _cart_id

import requests
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items:
                        variations = cart_item.variations.all()
                        product_variation.append(list(variations))

                    cart_items = CartItem.objects.filter(cart__user=user)
                    existing_variation_list = [list(item.variations.all()) for item in cart_items]
                    id = [item.id for item in cart_items]

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('account')
        else:
            messages.error(request=request, message="Login failed!")

    else:
        print('Error')

    context = {
        
    }
    return render(request, 'accounts/login.html', context=context)


def signup(request):
    print(request)
    if request.method == 'POST':
        form = request.POST

        full_name = form['full_name']
        email = form['email']
        password = form['password']
        password_confirmation = form['password_confirmation']
        print(full_name, email, password, password_confirmation)

        if password == password_confirmation:
            user = Account.objects.create_user(
                full_name=full_name,
                email=email,
                password=password
            )
            user.save()

            auth.login(request, user)
            return redirect('home')
        else:
            print('Password do not match')
    else:
        print('Error')
        return redirect('store')

    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user).order_by('-created_at')
    address = current_user.address
    province = current_user.province
    city = current_user.city

    context = {
        'user': current_user,
        'orders': orders,
        'address': address,
        'province': province,
        'city': city,
    }

    return render(request, 'accounts/account.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def wishlist(request):
    userWishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': userWishlist,
    }

    return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def add_wishlist(request):
    
    return redirect('wishlist')