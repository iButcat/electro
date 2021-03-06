from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy

from electro_social.models import Profile

from groups.models import Group


class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    post_img = models.ImageField(upload_to='img', blank=True, null=True)
    date_post = models.DateTimeField('date published',auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='likes',
    blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
    blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.user, self.title)

    class Meta:
        ordering = ['date_post']

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True,
    null=True)
    title = models.CharField(max_length=30)
    comment = models.TextField()
    date_post = models.DateTimeField('date published',auto_now_add=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, blank=True, null=True)
    like = models.ManyToManyField(User, related_name='comment_like',
    blank=True)

    def __str__(self):
        return "{}, {}".format(self.from_user, self.title)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.pk})
