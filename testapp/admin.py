from django.contrib import admin

from testapp.models import Blog, Post, Comment, PostPhoto

admin.site.register(Blog)
# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostPhoto)


class PostPhotoInlineAdmin(admin.StackedInline):
    model = PostPhoto


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostPhotoInlineAdmin]
