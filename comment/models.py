from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from post.models import Post

# Create your models here.
class Comment(models.Model):
  post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name='comments')
  content = models.TextField()
  author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments' )
  created_at = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f'id = {self.id}, author_id = {self.author.id}, post_id = {self.post.id}'