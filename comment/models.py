from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Comment(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.content