# Generated by Django 4.0 on 2022-01-26 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_country_order_province_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fullname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
