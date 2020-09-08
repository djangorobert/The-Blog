from django.contrib import admin
from posts.models import Post, PostView, Comment, Like
# Register your models here.


admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(Comment)
admin.site.register(Like)