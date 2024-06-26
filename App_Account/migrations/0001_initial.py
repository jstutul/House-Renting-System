# Generated by Django 3.2 on 2024-04-06 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[(1, 'House Owner'), (2, 'Renter')], default=2, max_length=10)),
                ('mobile', models.CharField(blank=True, max_length=15)),
                ('nid', models.CharField(blank=True, max_length=20)),
                ('photo', models.ImageField(blank=True, upload_to='user_photos/')),
                ('city', models.CharField(max_length=100)),
                ('present_address', models.TextField()),
                ('permanent_address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
