from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView,
FormView, SingleObjectMixin)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms.models import inlineformset_factory

from .forms import GroupFrom, PostForm
from .models import Group, Member

from django.contrib.auth.models import User
from electro_social.models import UserInfo

from posts.models import Post


# List of group
class GroupListView(ListView):

    template_name = 'group/index_group.html'
    model = Group
    context_object_name = 'groups'

    def get_success_url(self):
        return reverse_lazy('groups:detail')


# group detail with context data for add post in group
class GroupDetailView(DetailView):

    model = Group
    template_name = 'group/detail_group.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['form'] = PostForm()
        context['postgroup'] = Post.objects.filter(group=self.kwargs['pk'])
        return context


# Post in group
class PostGroupFormView(LoginRequiredMixin, SingleObjectMixin, FormView):

    model = Post
    form_class = PostForm
    template_name = 'group/detail_group.html'

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form = PostForm()
        if self.request.method == "POST":
            form = PostForm(self.request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.instance.group = self.get_object()
                form.instance.user = self.request.user
                form.save(commit=True)
        return super(PostGroupFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('groups:detail', kwargs={'pk': self.object.pk})


class MixinDetailAndFormView(View):

    def get(self, request, *args, **kwargs):
        view = GroupDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostGroupFormView.as_view()
        return view(request, *args, **kwargs)


# create group view
class CreateGroupView(CreateView):

    form_class = GroupFrom
    model = Group
    template_name = 'group/create_group.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            form.save()
        return super(CreateGroupView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('groups:detail', kwargs={'pk': self.object.pk})


# Join Group view
class JoinGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('groups:detail', kwargs=
        {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs.get('pk'))
        if not Member.objects.filter(group=group, user=self.request.user):
            obj, created = Member.objects.get_or_create(user=self.request.user,
            group=group)
            if created:
                messages.success(request, 'You are now a member')
        else:
            messages.add_message(request, messages.INFO, 'You are already a member')
        return super(JoinGroup, self).get(request, *args, **kwargs)


# leave group redirectview
class LeaveGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('groups:detail',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs.get('pk'))
        delete_member = Member.objects.filter(
        user=self.request.user, group=group).delete()
        if delete_member:
            messages.success(request, 'You leave the group')
        return super(LeaveGroup, self).get(request, *args, **kwargs)


# update group view
class UpdateGroupView(UpdateView):
    template_name = 'group/update_group.html'
    model = Group
    form_class = GroupFrom

    def get_success_url(self):
        return reverse_lazy('groups:detail', kwargs={'pk': self.object.pk})


# delete view
class DeleteGroupView(DeleteView):
    template_name = 'group/delete_group.html'
    model = Group
    success_url = reverse_lazy('groups:list')
