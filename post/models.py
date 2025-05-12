from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from tag.models import Tag
## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

