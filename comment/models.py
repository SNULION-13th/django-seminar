from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"content={self.content}, author={self.author.username}, post={self.post.title}"
