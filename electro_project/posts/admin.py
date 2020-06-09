from django.contrib import admin

from .models import Post, Commentary

class PostAdmin(admin.ModelAdmin):
    pass

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'date_post', 'post')
    search_fields = ('title', 'comment')


admin.site.register(Post, PostAdmin)
admin.site.register(Commentary, CommentaryAdmin)
