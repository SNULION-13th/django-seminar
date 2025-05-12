from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from post.models import Post

## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)

class Comment(models.Model):

    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title

