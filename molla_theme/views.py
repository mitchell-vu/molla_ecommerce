from django.shortcuts import render
from store.models import Product

# Create your views here.

def home(request):
  new_arrivals = [
    {
      'title': 'All',
      'id': 'new-all',
      'products': Product.objects.all(),
      'class': 'show active',
    },
    {
      'title': 'TV',
      'id': 'new-tv',
      'products': Product.objects.all(),
    },
    {
      'title': 'Computers',
      'id': 'new-computers',
      'products': Product.objects.all(),
    },
    {
      'title': 'Tablets & Cellphones',
      'id': 'new-phones',
      'products': Product.objects.all(),
    },
    {
      'title': 'Smartwatches',
      'id': 'new-watches',
      'products': Product.objects.all(),
    },
    {
      'title': 'Accessories',
      'id': 'new-acc',
      'products': Product.objects.all(),
    },
  ]

  trending_tab = [
    {
      'title': 'Top rated',
      'id': 'trending-top',
      'products': Product.objects.all(),
      'class': 'show active',
    },
    {
      'title': 'On sale',
      'id': 'trending-sale',
      'products': Product.objects.all(),
    },
  ]


  context = {
    'banners': [1, 1, 3],
    'categories': [1, 2, 3, 4, 5, 6],
    'new_arrivals': new_arrivals,
    'brands': [1, 2, 3, 4, 5, 6],
    'trending': trending_tab,
    'recommendations': Product.objects.all()[:8],
  }
  return render(request, 'home/home.html', context)


def error_404(request, exception):
  # print(exception)
  context = {}
  return render(request, 'home/404.html', context)


def contact(request):
  context = {}
  return render(request, 'home/contact.html', context)