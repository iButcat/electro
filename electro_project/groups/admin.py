from django.contrib import admin
from .models import Group, Member


class GroupAdmin(admin.ModelAdmin):
    pass


class MemberAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
