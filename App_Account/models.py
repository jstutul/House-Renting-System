from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
USER_TYPE_LIST = (
        ('1', 'House Owner'),
        ('2', 'Renter'),
    )
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userType = models.CharField(max_length=10, choices=USER_TYPE_LIST, default=2)
    mobile = models.CharField(max_length=15, blank=True)
    nid = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    city = models.CharField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return self.user.username
    
    def get_user_type(self):
        for choice in USER_TYPE_LIST:
            if int(choice[0]) == int(self.userType):
                return choice[1]
        return None
    def get_user_type_display(self, type=None):
        type_to_search = type if type else self.userType
        for choice in USER_TYPE_LIST:
            if choice[0] == type_to_search:
                return choice[1]
        return None

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()