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
from django.db.models import F

from . import forms
from .forms import UserInfoForm, UserProfileSearchForm
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
    form_class = UserProfileSearchForm
    template_name = 'users/user_profile.html'
    context_object_name = 'infos'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return UserInfo.objects.filter(user__username__icontains=form.cleaned_data['user'])
        return UserInfo.objects.all()


# this is where we fill the UserInfo => - description - profile pic
class UserInfoFormView(FormView, LoginRequiredMixin):

    template_name = 'users/user_form.html'
    model = UserInfo
    form_class = UserInfoForm

    def form_valid(self, form):
        form = UserInfoForm()
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
        return super(UserInfoFormView, self).form_valid(form)

    # suppose to send the success url but not working with args
    def get_success_url(self):
         return reverse_lazy("electro:detail", kwargs={'pk': self.kwargs})


# Detail of UserProfile with extra data => - Posts - Groups
class DetailUserProfile(DetailView):

    template_name = 'users/user_detail.html'
    model = UserInfo

    def get_object(self):
        return UserInfo.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailUserProfile, self).get_context_data(**kwargs)
        context['infos'] = self.get_object()
        context['posts'] = Post.objects.all().filter(user=self.kwargs['pk'])
        context['post_numbers'] = Post.objects.filter(user=self.kwargs['pk']).count()
        context['groups'] = Group.objects.filter(members=self.kwargs['pk'])
        context['friends'] = FriendRequest.objects.all()
        return context


#Update Userinfo
class UserInfoUpdate(UpdateView):
    template_name = 'users/user_update.html'
    model = UserInfo
    fields = ['description', 'profile_picture']

    def get_object(self):
        return UserInfo.objects.filter(user=self.kwargs['pk']).first()

    def form_valid(self, form):
        form = UserInfoForm()
        if self.request.method == "POST":
            form = UserInfoForm(self.request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = self.request.user
                profile.save()
        return super(UserInfoUpdate, self).form_valid(form)


# Delete user info
class UserInfoDelete(DeleteView):
    model = UserInfo
    success_url = reverse_lazy('users/user_profile.html')


# Send Friend request
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


# Accept Friend request
class AcceptFriendRequest(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('electro:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        friend_request = FriendRequest.objects.get(id=self.kwargs['pk'])
        user_one = request.user
        user_two = friend_request.from_user
        return super(AcceptFriendRequest, self).get(request, *args, **kwargs)
