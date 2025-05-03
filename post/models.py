## models > Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone


# Create your models here.
### 모델 ""상속"" 받아서 요소 적어주기. 기본적으로 장고에서 제공하는 '모델'이라는 라이브러리가 있음. 
class Post(models.Model):
		## title은 최대 256자의 character! 제목의 길이는 이걸 넘을 수 없다.
    title = models.CharField(max_length=256)
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title