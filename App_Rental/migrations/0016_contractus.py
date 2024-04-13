# Generated by Django 3.2 on 2024-04-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Rental', '0015_house_rent_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('message', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
