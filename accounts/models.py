from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from store.models import Product

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not email:
            raise ValueError('Email is required')
        if not full_name:
            raise ValueError('User name is required')

        user = self.model(
            # nomarlize_email để coi test@test.com với test@TEST.com là như nhau
            # Vì bình thường thì domain là case-insensitive
            email=self.normalize_email(email=email),
            full_name=full_name,
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Login field
    REQUIRED_FIELDS = ['full_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name