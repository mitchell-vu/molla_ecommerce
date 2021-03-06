# Generated by Django 4.0 on 2022-01-10 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_brand_variationcategory_variation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variationcategory',
            options={'verbose_name': 'variation category', 'verbose_name_plural': 'variation categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.brand'),
        ),
    ]
