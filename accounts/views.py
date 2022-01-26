from django.shortcuts import render
from orders.models import *

# Create your views here.


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

    return render(request, 'accounts/dashboard.html', context)


def login(request):
    context = {

    }

    return render(request, 'accounts/login.html', context)


def wishlist(request):
    context = {

    }

    return render(request, 'accounts/wishlist.html', context)
