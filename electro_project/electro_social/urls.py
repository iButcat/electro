from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'electro'

urlpatterns = [
  # auth system path => registration/(login.html and register.html)
  path('login', auth_views.LoginView.as_view(
  template_name ='registration/login.html',
  ), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('signup', views.SignUp.as_view(), name='signup'),
  # user info view and form => user_profile
  path('userform/', views.UserInfoFormView.as_view(),
  name='userform'),
  path('user', views.DisplayUserInfoView.as_view(), name='user'),
  path('user/<int:pk>/', views.DetailUserProfile.as_view(), name='detail'),
  # user update and delete => user_profile
  path('update/<int:pk>/', views.UserInfoUpdate.as_view(),
  name='update'),
  path('user/<int:pk>/delete/', views.UserInfoDelete.as_view(),
  name='delete'),
  # suppose to add friends
  path('add/<int:pk>/', views.SendFriendRequest.as_view(), name='add'),
  path('accept/<int:pk>', views.AcceptFriendRequest.as_view(), name='accept'),
]
