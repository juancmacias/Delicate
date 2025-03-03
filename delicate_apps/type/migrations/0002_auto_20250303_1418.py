from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('type', '0001_initial'),  # Asegúrate de que este nombre coincida con la migración anterior
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