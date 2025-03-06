# Generated by Django 5.1.6 on 2025-03-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_fix_empty_usernames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roll',
            field=models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('employee', 'Employee'), ('customer', 'Customer')], default='employee', max_length=50),
        ),
    ]
