from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import GroupFrom, PostInGroupForm
from .models import Group, Member

from django.contrib.auth.models import User
from electro_social.models import UserInfo

from posts.models import Post

class GroupListView(ListView):

    template_name = 'index_group.html'
    model = Group
    context_object_name = 'groups'

    def get_success_url(self):
        return reverse_lazy('groups:detail')


# group detail with context data for add post in group
class GroupDetailView(DetailView):

    model = Group
    template_name = 'detail_group.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['form'] = PostInGroupForm()
        context['postgroups'] = Group.objects.filter(post=self.kwargs['pk'])
        return context


# redirect for save post in group
class RedirectAddPostGroup(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('groups:detail',
        kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        # id=request.POST.get('post')
        obj, created = Group.objects.get_or_create(post=post)
        return super(RedirectAddPostGroup, self).get(request, *args, **kwargs)


# create group view
class CreateGroupView(CreateView):

    form_class = GroupFrom
    model = Group
    template_name = 'create_group.html'

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
        obj, created = Member.objects.get_or_create(user=self.request.user, group=group)
        #Member.objects.create(user=self.request.user, group=group)
        return super(JoinGroup, self).get(request, *args, **kwargs)


# leave group redirectview
class LeaveGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('groups:detail',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs.get('pk'))
        Member.objects.filter(user=self.request.user, group=group).delete()
        return super(LeaveGroup, self).get(request, *args, **kwargs)


# update group view
class UpdateGroupView(UpdateView):
    template_name = 'update_group.html'
    model = Group
    form_class = GroupFrom

    def get_success_url(self):
        return reverse_lazy('groups:detail', kwargs={'pk': self.object.pk})


# delete view
class DeleteGroupView(DeleteView):
    template_name = 'delete_group.html'
    model = Group
    success_url = reverse_lazy('groups:list')
