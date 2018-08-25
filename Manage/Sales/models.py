from django.db import models

# Create your models here.



class Account(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=400)
    user_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Outlets(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lat = models.CharField(max_length=400)
    long = models.CharField(max_length=400)
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    image = models.FileField(blank=True)
    outlet = models.ForeignKey(Outlets,on_delete=models.CASCADE)
    grade = models.CharField(max_length=200,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.outlet.name


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


