from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
  list_display = ('full_name', 'email', 'phone')

class OrderProductAdmin(admin.ModelAdmin):
  list_display = ('order', 'product', 'quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment)
