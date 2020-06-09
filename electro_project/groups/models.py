from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from electro_social.models import UserInfo
from posts.models import Post


class Group(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, through='Member')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, blank=True, null=True, related_name='owner')
    post = models.ForeignKey(Post, blank=True, null=True,
    on_delete=models.CASCADE)

    def __str__(self):
        return "{}, title: {}".format(self.owner, self.title)

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.pk})


class Member(models.Model):
    group = models.ForeignKey(Group, related_name="memberships",
    on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_groups",
    on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        unique_together = ("group", "user")
