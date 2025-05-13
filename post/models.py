from django.db import models
# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone
from django.contrib.auth.models import User # <- 추가
## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=256)
  ## content는 글자 제한 없는 텍스트
  content = models.TextField()
  
  ## created_at의 경우는 현재 시간 자동으로 입력되게!
  created_at = models.DateTimeField(default=timezone.now)
  #OneToMany관계일 때, Many(자식)쪽에 One(부모)를 foreignKey로 추가
  author = models.ForeignKey(User, null=  True, on_delete = models.CASCADE) #User객체가 삭제되는 경우, 연결된 Post객체도 삭제되도록 하는 옵션
  #related_name: User에서 post역참조 가능
  #through : 중계테이블 모델 지정. 지정해주지 않으면 자동으로 생성됨
  like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')
  #둘 중 한쪽에 ManyToManyField를 지정해주면 장고가 자동으로 중계 테이블을 만들어준다. (즉, tag앱쪽에 작성해도 상관없음)
  tags = models.ManyToManyField('tag.Tag' , blank = True, related_name = 'posts')
  
  ## 이건 print하면 어떤 값을 return할 지 알려주는 것!
  def __str__(self):
      return self.title
  
#실제 현업에서의 활용! 중계 테이블을 만들고, ManyToManyField에 직접 만든 중계 테이블을 지정해준다.
# 중계 테이블: Like. 어떤 Post와 어떤 User가 연결되어있는지를 관리한다.   
class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)