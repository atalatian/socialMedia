from django.contrib import admin
from .models import User, Post, UserJoin, Like, Comment
admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserJoin)
admin.site.register(Like)
admin.site.register(Comment)

# Register your models here.
