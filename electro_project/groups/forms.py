from .models import Group
from django import forms

from django.forms import ModelForm

from posts.models import Post

class GroupFrom(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'description']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class PostInGroupForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets= {
        'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }
