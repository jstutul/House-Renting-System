# Generated by Django 3.2 on 2024-04-07 19:04

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Rental', '0006_house_map_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='advacne_rent',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
