from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'date_post', 'post')
    search_fields = ('title', 'comment')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
