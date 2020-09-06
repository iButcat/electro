from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import Profile


class UserCreateForm(UserCreationForm):
    username = forms.CharField(
    widget=forms.TextInput(
    attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    email = forms.EmailField(widget=(forms.TextInput(
    attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=('Password'),
    widget=(forms.PasswordInput
    (attrs={'class': 'form-control'})))
    password2 = forms.CharField(label=('Password Confirmation'),
    widget=forms.PasswordInput(
    attrs={'class': 'form-control'}))


    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'username'
        self.fields['email'].label = 'email'


class UserUpdateForm(UserChangeForm):
    class Meta:
        fields = ('username', 'email')
        model = User

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].label = 'username'
            self.fields['email'].label = 'email'


class UserInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'description', 'birth_date']


class UserProfileSearchForm(forms.Form):
    user = forms.CharField(required=False)
