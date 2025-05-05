from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
		## title은 최대 256자의 character!
    title = models.CharField(max_length=256)
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title