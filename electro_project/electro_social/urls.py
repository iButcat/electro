from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'electro'

urlpatterns = [
  # auth system
  path('login/', auth_views.LoginView.as_view(
  template_name ='registration/login.html',
  ), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('signup/', views.SignUp.as_view(), name='signup'),
  path('update_settings/', views.UserEdit.as_view(), name="update_settings"),
  path('password/', views.PasswordChangeView.as_view(
  template_name="registration/change_password.html"
  ), name='password'),
  path('users/', views.ProfileList.as_view(), name='users'),
  path('user/<int:pk>/', views.ProfileDetail.as_view(), name='detail'),
  # user update and delete => user_profile
  path('update/<int:pk>/', views.ProfileUpdate.as_view(),
  name='update'),
  path('user/<int:pk>/delete/', views.ProfileUpdate.as_view(),
  name='delete'),
  path('follow/<int:pk>', views.FollowProfileRedirect.as_view(), name="follow"),
]
