from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy

from PIL import *

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='img', blank=True, null=True)
    description = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followers")

    def __str__(self):
        return "@{}".format(self.user)

    class Meta():
        ordering = ['user']

    def get_absolute_url(self):
        return reverse_lazy('electro:detail', kwargs={'pk': self.pk})

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
