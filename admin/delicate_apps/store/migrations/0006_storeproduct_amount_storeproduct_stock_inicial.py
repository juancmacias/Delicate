# Generated by Django 5.1.6 on 2025-03-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_organize_stock_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproduct',
            name='amount',
            field=models.CharField(default='', max_length=100, verbose_name='Cantidad (obsoleto)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='stock_inicial',
            field=models.IntegerField(default=0, verbose_name='Stock inicial (obsoleto)'),
        ),
    ]
