## models > Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone

from django.contrib.auth.models import User # <- 추가

from tag.models import Tag # Tag를 불러와서 Post에서 어쩌구 저쩌구 하려고. model끼리 연결하는 느낌.

# Create your models here.
### 모델 ""상속"" 받아서 요소 적어주기. 기본적으로 장고에서 제공하는 '모델'이라는 라이브러리가 있음. 
class Post(models.Model):
		## title은 최대 256자의 character! 제목의 길이는 이걸 넘을 수 없다.
    title = models.CharField(max_length=256)
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)
    
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # 왜 userprofile 모델이 아니라 user를 추가하는걸까.
    # user를 연결하는게 훨씬 편하대. userprofile로 하면 또 그걸 get으로 가져오고 어쩌구 해야하는... user는 기본 저장 라이브러리라 바로 가져올 수 있대.
    
    # 또 attribute로 따로 user를 만드는 것이 아니라 따로 모델을 만들어서 거기서 불러오는게 메모리 측면에서 낫다.

    like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')
    # 지피티 왈 : 이건 "이 포스트를 좋아요한 사용자들"을 쉽게 조회하기 위한 shortcut 필드
    # 장고에게 선언해준다. Post와 User는 manytomany 관계인데, 중간 테이블로는 Like 모델을 써달라!
    # like_posts는 Like 모델 쪽에서도 자동 생성된 manytomany field.
    # 이제 post.like_users.all(), user.like_posts.all() 등을 조회가 가능하다. 
    # 이 manyTomany 선언이 없으면 무조건 Like.objects.filter(post=...)처럼 직접 쿼리를 써야 한다. 번거로운거지.
    # 지금은 중간 테이블로 "Like 모델"을 사용했는데, 이걸 명시적으로 안정해주고 자동으로 만들어달라고 할 수도 있다.
    
    
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    # manyTomany : 하나의 게시글은 여러 태그를 가질 수 있고, 한 태그는 동시에 여러개의 게시글에 붙을 수 있죠. 즉, 게시글과 태그는 ManyToMany 관계
    # Post와 Tag는 manyToMany 관계라는 것이다!!
    # Like와 다른 점은 Like는 many to 1 느낌이었음.. 그래서 manyTomany에다가 through를 붙인다는거!
    
		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title
      
      
# like 모델 추가. like 데이터 베이스에 들어갈 내용들. 어떤 포스트에서 / 어떤 유저가 누른건지. 
# --> 같은 포스트에 대한 것만 뭔가 sum을 해서 표현을 하면 되겟지.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)