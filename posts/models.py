from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    # to delete the post when the user is deleted
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-created']

     # self = Course model and passing name to admin
    def __str__(self):
        return self.title

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.voter