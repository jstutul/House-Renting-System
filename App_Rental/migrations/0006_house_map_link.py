# Generated by Django 3.2 on 2024-04-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Rental', '0005_auto_20240407_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='map_link',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
