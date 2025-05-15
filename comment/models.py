from django.db import models

# Create your models here.
from django.utils import timezone
from post.models import Post
from django.contrib.auth.models import User # 디폴트로 제공하는 user 모델을 불러오기

# User와 Post를 모두 foreign 키로 받아오기 위해서 둘 다 import



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # User로 연결하는게 편해서 User를 foreign키로. 나중에 참조할 수 있도록.
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    # str은 일단 생략