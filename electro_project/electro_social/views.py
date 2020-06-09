from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import (FormView, SingleObjectMixin,
CreateView, DeleteView, UpdateView)
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import models

from . import forms
from .forms import UserInfoForm
from .models import UserInfo, FriendRequest

from posts.models import Post, Commentary
from groups.models import Group


# Create an account => signup
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


# list of all users available
class DisplayUserInfoView(ListView):
    model = UserInfo
    template_name = 'users/user_profile.html'
    context_object_name = 'infos'


# this is where we fill the UserInfo => - description - profile pic
class UserInfoFormView(FormView, LoginRequiredMixin):
    template_name = 'users/user_form.html'
    model = UserInfo
    form_class = UserInfoForm

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(UserInfoForm, self).form_valid(form)

    # suppose to send the success url but not working with args
    def get_success_url(self):
         return reverse_lazy("electro:detail", kwargs={'pk': self.kwargs['pk']})


# Detail of UserProfile with extra data => - Posts - Groups
# User's post only showing one post, must be fix
class DetailUserProfile(DetailView):

    template_name = 'users/user_detail.html'
    model = UserInfo
    #context_object_name = 'info'

    def get_object(self):
        return UserInfo.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailUserProfile, self).get_context_data(**kwargs)
        context['infos'] = self.get_object()
        posts = Post.objects.filter(pk=self.kwargs['pk'])
        context['posts'] = posts
        post_numbers = Post.objects.filter(user=self.request.user).count()
        context['post_numbers'] = post_numbers
        groups = Group.objects.filter(pk=self.kwargs['pk'])
        context['groups'] = groups
        friends = FriendRequest.objects.all()
        context['friends'] = friends
        return context


#Update Userinfo => must be finish
class UserInfoUpdate(UpdateView):
    template_name = 'users/user_update.html'
    model = UserInfo
    fields = ['description', 'profile_picture']


# Delete user info
class UserInfoDelete(DeleteView):
    model = UserInfo
    success_url = reverse_lazy('users/user_profile.html')


# working but adding the user who request
class SendFriendRequest(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('electro:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(UserInfo, id=self.kwargs.get(('pk')))
        obj, created = FriendRequest.objects.get_or_create(
        from_user = self.request.user,
        to_user=user)
        return super(SendFriendRequest, self).get(request, *args, **kwargs)


class AcceptFriendRequest(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('electro:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        friend_request = FriendRequest.objects.get(id=self.kwargs['pk'])
        user_one = request.user
        user_two = friend_request.from_user
        return super(AcceptFriendRequest, self).get(request, *args, **kwargs)
