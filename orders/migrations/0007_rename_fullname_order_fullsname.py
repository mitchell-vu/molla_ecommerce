# Generated by Django 4.0 on 2022-01-26 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_fullname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='fullname',
            new_name='full_name',
        ),
    ]