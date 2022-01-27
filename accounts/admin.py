from django.contrib import admin
from accounts.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'last_login', 'date_joined')
    # Các trường có gắn link dẫn đến trang detail
    list_display_links = ('email', 'full_name')   
    readonly_fields = ('last_login', 'date_joined')   
    ordering = ('-date_joined',)     

    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Wishlist)