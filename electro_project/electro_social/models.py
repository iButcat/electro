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


class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='img', blank=True)
    description = models.TextField(blank=True)
    friends = models.ManyToManyField('UserInfo', blank=True)

    def __str__(self):
        return "@{}".format(self.user)

    class Meta():
        ordering = ['user']

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserInfo.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userinfo.save()

    def get_absolute_url(self):
        return reverse_lazy('electro:detail', kwargs={'pk': self.pk})


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
    related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserInfo,
    related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return "@{} to  @{}".format(self.from_user, self.to_user)
