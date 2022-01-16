from django.db import models
from store.models import *
from accounts.models import *

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def sub_total(self):
        cart_items = CartItem.objects.filter(cart=self)
        return sum([cart_item.sub_total() for cart_item in cart_items])


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # 1 máy điện thoại có thể có 2 variations như Storage và Color
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name

    def sub_total(self):
        return self.quantity * self.product.price