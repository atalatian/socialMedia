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

    def get_users_by_user_pk(self, user_pk):
        return UserJoin.objects.filter(user_id=user_pk)

    def get_users_by_following_pk(self, following_pk):
        return UserJoin.objects.filter(following_id=following_pk)

    def get_users_by_both(self, user_pk, following_pk):
        return UserJoin.objects.get(user_id=user_pk, following_id=following_pk)

    def create_join(self, user_pk, following_pk):
        UserJoin(user_id=user_pk, following_id=following_pk).save()

    def delete_join(self, user_pk, following_pk):
        self.get_users_by_both(user_pk, following_pk).delete()


class PostManager(models.Manager):
    def get_posts_by_user_pk(self, user_pk):
        return Post.objects.filter(user_id=user_pk)


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likePost.count()

    def user_can_like(self, user):
        user_like = user.likeUser.all()
        qs = user_like.filter(post=self)
        if qs.exists():
            return True
        return False

    objects = models.Manager()
    myObjects = PostManager()


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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likePost')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likeUser')

    def __str__(self):
        return f'{self.user} liked {self.post}'
