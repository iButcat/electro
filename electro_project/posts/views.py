from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView, SingleObjectMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic.base import RedirectView

from .forms import UserCommentForm, UserPostForm
from .models import Post, Commentary

from electro_social.views import DetailUserProfile
from electro_social.models import UserInfo


# see all the post
class PostListView(ListView):

    template_name = 'logged/post_list.html'
    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(date_post__lte=timezone.now()).order_by(
                '-date_post')

    def get_success_url(self):
        return reverse_lazy('posts:detail')


# => Create post
class CreatePostView(LoginRequiredMixin, CreateView):

    login_url = 'electro/login'
    template_name = 'logged/create_post.html'
    form_class = UserPostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        pk = self.kwargs.get("post_pk", None)
        form.instance.post = pk
        if form.is_valid():
            form.save()
            return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        return reverse("posts:detail", kwargs={'pk': self.object.pk})


# => Update post view
class UpdatePostView(LoginRequiredMixin, UpdateView):

    login_url = 'electro/login'
    template_name = 'logged/post_update.html'
    form_class = UserPostForm
    model = Post

    def get_object(self, queryset=None):
        return Post.objects.filter(pk=self.kwargs['pk']).first()

    # filter if the current user is the author
    def get_queryset(self):
        queryset = super(UpdatePostView, self).get_queryset()
        queryset = queryset.filter(from_user=self.request.user)
        return queryset

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super(UpdatePostView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


# => Delete Post
class DeletePostView(LoginRequiredMixin, DeleteView):

    template_name = 'logged/post_delete.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, queryset=None):
        return Post.objects.filter(pk=self.kwargs['pk']).first()

    def get_queryset(self):
        queryset = super(DeletePostView, self).get_queryset()
        queryset = queryset.filter(from_user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('posts:list')


# 3 part => Mixed views
# 1 part => detail view with context data for forms and comments
class PostDetailView(DetailView):

    template_name = 'logged/post_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = Commentary.objects.filter(post=self.kwargs['pk'])
        context['comments'] = comments
        context['form'] = UserCommentForm()
        return context


# 2 part => Form view for comments
class CommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):

    template_name = 'logged/post_detail.html'
    model = Commentary
    form_class = UserCommentForm

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        form.instance.post = self.get_object()
        if form.is_valid():
            form.save()
            return super(CommentFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:detail", kwargs={'pk': self.kwargs['pk']})


# part 3 => this is where we send both view in one
class PostCommentFormView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


# like redirect suppose to be redirect to detail post which was liked
class RedirectAddLike(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('posts:detail', kwargs=
        {'pk': self.kwargs.get('pk')})


    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post.like.add(self.request.user)
        return super(RedirectAddLike, self).get(request, *args, **kwargs)


class RedirectAddDislike(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('posts:detail', kwargs=
                            {'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post.like.remove(self.request.user)
        return super(RedirectAddDislike, self).get(request, *args, **kwargs)
