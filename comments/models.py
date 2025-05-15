from django.db import models
from django.contrib.auth.models import User 
from post.models import Post
from django.utils import timezone
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comment_author')
    created_at = models.DateTimeField(default=timezone.now)
