from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
  path('create/', views.CreateGroupView.as_view(), name='create'),
  path('list/', views.GroupListView.as_view(), name='list'),
  path('detail/<int:pk>', views.GroupDetailView.as_view(), name='detail'),
  path('join/<int:pk>', views.JoinGroup.as_view(), name='join'),
  path('leave/<int:pk>', views.LeaveGroup.as_view(), name='leave'),
  path('update/<int:pk>', views.UpdateGroupView.as_view(), name='update'),
  path('delete/<int:pk>', views.DeleteGroupView.as_view(), name='delete'),
  path('detail/<int:pk>', views.RedirectAddPostGroup.as_view(), name='redirect')
]
