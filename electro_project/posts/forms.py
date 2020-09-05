from django.forms import ModelForm
from django import forms
from .models import Commentary, Post


class UserPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserCommentForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ['title', 'comment']
        exclude = ['group']

        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
