# Generated by Django 5.1.6 on 2025-03-05 13:13

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_storeproduct_amount_storeproduct_stock_inicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeproduct',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Imagen del producto', max_length=255, null=True, verbose_name='image'),
        ),
    ]
