from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag

# Create your models here.
class Post(models.Model):
		## title은 최대 256자의 character!
    title = models.CharField(max_length=256)
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

    ## 작성자정보
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    ## 포스트에 좋아요를 누른 사람들
    like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')

    ## 태그
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)