from django.contrib import admin
from .models import User
from .models import Post
from .models import UserJoin
admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserJoin)

# Register your models here.
