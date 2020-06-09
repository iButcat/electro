from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserInfo, FriendRequest


class UserInfoAdmin(admin.ModelAdmin):
    pass


class FriendRequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
