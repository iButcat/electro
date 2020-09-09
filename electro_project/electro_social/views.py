from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import (
FormView,
SingleObjectMixin,
CreateView,
DeleteView,
UpdateView
)
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.contrib import messages
from .forms import (
UserCreateForm,
UserInfoForm,
UserProfileSearchForm,
UserUpdateForm
)
from .models import Profile

from posts.models import Post, Comment
from groups.models import Group


class SignUp(CreateView):
    form_class = UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEdit(UpdateView):
    form_class = UserUpdateForm
    template_name = 'registration/update_user.html'
    success_url = reverse_lazy('posts:list')

    def get_object(self):
        return self.request.user

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')


class ProfileList(ListView):
    model = Profile
    form_class = UserProfileSearchForm
    template_name = 'profiles/profile_list.html'
    context_object_name = 'infos'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Profile.objects.filter(
            user__username__icontains=form.cleaned_data['user']
            )
        return Profile.objects.all()


class ProfileDetail(DetailView):
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        return Profile.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['infos'] = self.get_object() # profile
        context['posts'] = Post.objects.all().filter(user=self.kwargs['pk'])
        context['post_numbers'] = Post.objects.filter(user=self.kwargs['pk']).count()
        context['groups'] = Group.objects.filter(members=self.kwargs['pk'])
        return context


class ProfileUpdate(UpdateView):
    template_name = 'profiles/profile_update.html'
    model = Profile
    fields = ['description', 'profile_picture']

    def form_valid(self, form):
        if self.request.method == "POST":
            obj = get_object_or_404(Profile, pk=self.kwargs['pk'])
            form = UserInfoForm(self.request.POST, instance=obj)
            if form.is_valid():
                form.save(commit=True)
        return super(ProfileUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("electro:detail", kwargs={'pk': self.kwargs.get('pk')})


class ProfileDelete(DeleteView):
    model = Profile
    success_url = reverse_lazy('profiles/profile_list.html')


class FollowProfileRedirect(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('electro:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        if self.request.method == "POST":
            my_profile = Profile.objects.get(user=self.request.user)
            pk = request.POST.get('pk')
            obj = Profile.objects.get(pk=pk)
            if obj.user in my_profile.followers.all():
                my_profile.followers.remove(obj.user)
                messages.success(request, 'WOW you are unfollowing {}'.format(
                my_profile.user))
            else:
                my_profile.followers.add(obj.user)
                messages.success(request, 'WOW you are following {}'.format(
                my_profile.user))
        return super(FollowProfileRedirect, self).get(request, *args, **kwargs)
