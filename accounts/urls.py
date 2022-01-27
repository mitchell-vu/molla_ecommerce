from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.dashboard, name='account'),
    path('dashboard/', views.dashboard, name='add_cart'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
]