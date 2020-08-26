from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'groups'

urlpatterns = [
  # group url
  path('create/', views.CreateGroupView.as_view(), name='create'),
  path('list/', views.GroupListView.as_view(), name='list'),
  path('join/<int:pk>', views.JoinGroup.as_view(), name='join'),
  path('leave/<int:pk>', views.LeaveGroup.as_view(), name='leave'),
  path('update/<int:pk>', views.UpdateGroupView.as_view(), name='update'),
  path('delete/<int:pk>', views.DeleteGroupView.as_view(), name='delete'),
  path('detail/<int:pk>', views.MixinDetailAndFormView.as_view(), name='detail'),
  path('user/<int:pk>', RedirectView.as_view(pattern_name='electro:detail'), name='redirect'), 
]
