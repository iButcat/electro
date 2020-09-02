from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import (FormView, SingleObjectMixin,
CreateView, DeleteView, UpdateView)
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.contrib import messages

from .forms import UserCreateForm
from .forms import UserInfoForm, UserProfileSearchForm
from .models import Profile

from posts.models import Post, Commentary
from groups.models import Group


# Create an account => signup
class SignUp(CreateView):
    form_class = UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

# list of all users available
class DisplayUserInfoView(ListView):
    model = Profile
    form_class = UserProfileSearchForm
    template_name = 'users/user_profile.html'
    context_object_name = 'infos'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Profile.objects.filter(
            user__username__icontains=form.cleaned_data['user']
            )
        return Profile.objects.all()


# this is where we fill the UserInfo => - description - profile pic
class UserInfoFormView(FormView, LoginRequiredMixin):
    template_name = 'users/user_form.html'
    model = Profile
    form_class = UserInfoForm

    def get_object(self):
        return Profile.objects.filter(pk=self.request.user.pk)

    def form_valid(self, form):
        form = UserInfoForm()
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
        return super(UserInfoFormView, self).form_valid(form)

    # need to repear, supposte to redirect user detail.
    def get_success_url(self):
         return reverse_lazy("electro:detail", kwargs={'pk': self.pk})


# Detail of UserProfile with extra data => - Posts - Groups
class DetailUserProfile(DetailView):
    template_name = 'users/user_detail.html'

    def get_object(self):
        return Profile.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailUserProfile, self).get_context_data(**kwargs)
        context['infos'] = self.get_object()
        context['posts'] = Post.objects.all().filter(user=self.kwargs['pk'])
        context['post_numbers'] = Post.objects.filter(user=self.kwargs['pk']).count()
        context['groups'] = Group.objects.filter(members=self.kwargs['pk'])
        return context


#Update Userinfo
class UserInfoUpdate(UpdateView):
    template_name = 'users/user_update.html'
    model = Profile
    fields = ['description', 'profile_picture']

    def get_object(self):
        return Profile.objects.filter(user=self.kwargs['pk']).first()

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
    model = Profile
    success_url = reverse_lazy('users/user_profile.html')


class FollowUserView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('electro:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        if request.method == "POST":
            my_profile = Profile.objects.get(user=self.request.user)
            pk = request.POST.get('profile_pk')
            obj = Profile.objects.get(pk=pk)
            if obj.user in my_profile.followers.all():
                my_profile.followers.remove(obj.user)
                messages.success(request, 'WOW you are unfollowing {}'.format(
                my_profile.user))
            else:
                my_profile.followers.add(obj.user)
                messages.success(request, 'WOW you are following {}'.format(
                my_profile.user))
        return super(FollowUserView, self).get(request, *args, **kwargs)
