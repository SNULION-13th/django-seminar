from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from post.models import Post


# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
