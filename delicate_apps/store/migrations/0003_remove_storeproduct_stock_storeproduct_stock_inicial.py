# Generated by Django 5.1.6 on 2025-03-03 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_storeproduct_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeproduct',
            name='stock',
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='stock_inicial',
            field=models.IntegerField(default=0, verbose_name='Stock inicial'),
        ),
    ]
