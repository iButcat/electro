from django.forms import ModelForm
from django import forms
from .models import Commentary, Post


class UserPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class UserCommentForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ['title', 'comment']
        exclude = ['group']

        widgets = {
        'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        'comment': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
