# Generated by Django 4.0 on 2022-01-27 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variation',
            name='price_offset',
            field=models.IntegerField(default=0),
        ),
    ]
