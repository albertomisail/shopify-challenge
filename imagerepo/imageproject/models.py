from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
class Image(models.Model): 
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    publish_date = models.DateTimeField('date published')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=999, decimal_places=2, default=0)
    deleted = models.BooleanField(default=False)

    def __str__(self): 
        return self.title

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    bought_date = models.DateTimeField('date bought')

# model to store additional non-authentication information about a user
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=999, decimal_places=2, default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
