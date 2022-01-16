from django.contrib import admin
from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),

    path('api/add_cart/<int:product_id>/', api.add_cart, name='api_add_cart'),
    path('api/update_cart/', api.update_cart, name='api_update_cart'),

    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]