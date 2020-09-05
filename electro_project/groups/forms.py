from .models import Group
from django import forms

from django.forms import ModelForm

from posts.models import Post

class GroupFrom(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'description']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
