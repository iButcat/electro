from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy


from . import views

app_name = 'posts'

urlpatterns = [
  # post list
  path('list/', views.PostListView.as_view(), name="list"),
  # post create
  path('create/', views.CreatePostView.as_view(), name='create'),
  # post update
  path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update'),
  # post delete
  path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete'),
  # post detail
  path('detail/<int:pk>/', views.PostCommentFormView.as_view(), name='detail'),
  # redirect user detail
  path('user/<int:pk>/', views.RedirectView.as_view(
  pattern_name='electro:detail', permanent=False), name='redirect'),
  # add like on post
  path('like/<int:pk>', views.RedirectAddLike.as_view(), name='like'),
  path('dislike/<int:pk>', views.RedirectAddDislike.as_view(), name='dislike')
]
