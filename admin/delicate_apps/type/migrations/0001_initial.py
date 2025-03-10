from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_type', models.CharField(max_length=30, verbose_name='Tipo de comercio')),
            ],
            options={
                'verbose_name': 'Tipo de comercio',
                'verbose_name_plural': 'Tipos de comercio',
                'db_table': 'type',
            },
        ),
    ]