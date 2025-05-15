# from django.db import models

# Create your models here.

# '앱'과 '모델'은 다른 개념. 하나의 앱에는 여러 모델이 존재 가능. 모델이란건 db와 파이썬을 이어주는건데, 데이터들의 형태를 정해주는 것.
# 여러 모델이 여러 DB에 매핑될 필요는 없음. 하나의 DB에서 여러 모델이 생성 가능. 그렇지만 다양한 데이터 형태를 가질 수 있음. DB에서 알아서 구분을 해서 저장해줌.

# django는 기본적으로 user 모델을 제공하고 있다. -> UserProfile은은 user를 약간 상속해서 뭔가 속성들을 추가하는 그런 느낌.


from django.db import models
from django.contrib.auth.models import User # 디폴트로 제공하는 user 모델을 불러오기

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 디폴트 User 모델을 불러와서 UserProfile에서 그걸 수정하게끔.
    # User와 UserProfile이 무조건 1ㄷ1 대응으로 매칭되도록 1t1 field 함수 사용.
    college = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"id={self.id}, user_id={self.user.id}, college={self.college}, major={self.major}"
    # str은 print(userProfile)하면 객체 정보들 반환.