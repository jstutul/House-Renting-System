from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from ckeditor.fields import RichTextField
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
HOUSE_TYPE_LIST = (
        ('1', 'Apartment'),
        ('2', 'Building'),
    )
class House(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=False)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=500, blank=False)
    house_type = models.CharField(max_length=10, choices=HOUSE_TYPE_LIST, default="1")
    house_name = models.CharField(max_length=200, null=True)
    house_area = models.IntegerField(default=800)
    description = RichTextField(null=True)
    is_parking = models.BooleanField(default=True)
    total_bedrooms = models.IntegerField(default=0)
    total_bathrooms = models.IntegerField(default=0)
    floor_no = models.IntegerField(default=0)
    map_link =models.CharField(max_length=10000,blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    advacne_rent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    images = models.ManyToManyField('HouseImage', related_name='houses', blank=True)
    is_active=models.BooleanField(default=False)
    is_reject=models.BooleanField(default=False)
    is_rented=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.title
class HouseImage(models.Model):
    image = models.ImageField(upload_to='house_photos/')

    def __str__(self):
        return f"Image {self.id}"


class HouseComment(models.Model):
    post = models.ForeignKey(House,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('HouseComment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title,str(self.post.owner))