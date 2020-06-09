from django import template

from posts.models import Post

register = template.Library()

@register.filter(name='cut')
def cut_post_group(value):
    return Post.objects.exclude(group=True)
