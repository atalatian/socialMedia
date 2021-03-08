from django.db import models


# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class UserJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="following")

    def __str__(self):
        return str(self.user) + " follows " + str(self.following)


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likepost.count()

    def user_can_like(self, user):
        user_like = user.likeuser.all()
        qs = user_like.filter(post=self)
        if qs.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:20]}'

    class Meta:
        ordering = ('-created',)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likepost')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likeuser')

    def __str__(self):
        return f'{self.user} liked {self.post}'