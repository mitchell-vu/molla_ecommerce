from django.shortcuts import redirect, render
from .models import *
from category.models import Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.


def store(request, category_slug=None):
    category = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category)
    else:
        products = Product.objects.all()

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 8)
    # paged_products = paginator.page(page).object_list
    paged_products = paginator.get_page(page)
    product_count = products.count()
    brands = Brand.objects.all()

    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'category': category,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'store/category.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(
        category__slug=category_slug,
        slug=product_slug
    )
    recommendations = Product.objects.all()
    colors = single_product.variation_set.filter(variation_category__category_name='Color')
    print(colors)
    context = {
        'single_product': single_product,
        'recommendations': recommendations,
        'colors': colors,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        products = Product.objects.filter(
            Q(product_name__icontains=q) |
            Q(description__icontains=q)
        )

        product_count = products.count()

        page = request.GET.get('page')
        page = page or 1
        paginator = Paginator(products, 8)
        paged_products = paginator.get_page(page)
    else:
        return redirect('store')

    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'category': 'Tìm kiếm',
        'categories': categories,
    }
    return render(request, 'store/category.html', context)
