from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title