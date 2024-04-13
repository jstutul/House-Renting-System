from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from ckeditor.fields import RichTextField
from django.utils import timezone
from datetime import timedelta

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
    def next_month_first_day():
        today = timezone.localdate()
        # Calculate the first day of next month
        first_day_next_month = today.replace(day=1) + timedelta(days=32 - today.day)
        return first_day_next_month
     
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=False)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=500, blank=False)
    rent_from = models.DateField(default=next_month_first_day)
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
  

class HouseRent(models.Model):
    post = models.ForeignKey(House,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=1000)
    created =models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title,self.user)
    def due_amount(self):
        return self.post.monthly_rent-self.post.advacne_rent
    

class ContractUs(models.Model):
    name = models.CharField(max_length=50,blank=False)
    email = models.EmailField(max_length=50,blank=False)
    message = models.TextField(max_length=500,blank=False)
    created = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.name,self.message)