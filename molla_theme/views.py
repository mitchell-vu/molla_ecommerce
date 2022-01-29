from django.shortcuts import render
from store.models import Product

# Create your views here.

def home(request):
  new_arrivals = [
    {
      'title': 'Tất cả',
      'id': 'new-all',
      'products': Product.objects.all(),
      'class': 'show active',
    },
    {
      'title': 'Điện thoại',
      'id': 'new-phone',
      'products': Product.objects.filter(category__slug='dien-thoai'),
    },
    {
      'title': 'Laptop',
      'id': 'new-computers',
      'products': Product.objects.filter(category__slug='laptop'),
    },
    {
      'title': 'Máy tính bảng',
      'id': 'new-tablet',
      'products': Product.objects.filter(category__slug='may-tinh-bang'),
    },
    {
      'title': 'Đồng hồ',
      'id': 'new-watches',
      'products': Product.objects.filter(category__slug='dong-ho-thong-minh'),
    },
    {
      'title': 'Phụ kiện',
      'id': 'new-acc',
      'products': Product.objects.filter(category__slug='phu-kien'),
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
      'products': Product.objects.filter(),
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