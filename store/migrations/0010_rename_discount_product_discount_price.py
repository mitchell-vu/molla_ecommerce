# Generated by Django 3.2.9 on 2022-01-28 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_discount_variation_price_offset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount',
            new_name='discount_price',
        ),
    ]
