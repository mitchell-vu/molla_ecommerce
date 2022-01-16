import os
from django.db import models
from django.db.models.deletion import CASCADE
from category.models import *

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.brand_name


def get_upload_path(instance, filename):
    return os.path.join(
        'photos',
        'products',
        instance.product.slug,
        filename
    )


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    # Khi xóa Category thì Product bị xóa
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


class VariationCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    display = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'variation category'
        verbose_name_plural = 'variation categories'


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.ForeignKey(
        VariationCategory, on_delete=CASCADE)
    variation_value = models.CharField(max_length=100)
    variation_image = models.ImageField(upload_to=get_upload_path, null=True)
    stock = models.IntegerField()

    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value
