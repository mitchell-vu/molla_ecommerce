from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category',
                    'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'display')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)   # Cho phép chỉnh sửa trên list hiển thị
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Variation, VariationAdmin)
admin.site.register(VariationCategory, VariationCategoryAdmin)