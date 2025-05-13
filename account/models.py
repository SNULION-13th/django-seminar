from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
  #OneToOneField이므로 상호 접근 가능
  user = models.OneToOneField(User, on_delete=models.CASCADE) #User 객체가 삭제가 된다면 UserProfile객체도 삭제되도록 하는 옵션
  college = models.CharField(max_length=32, blank=True)
  major = models.CharField(max_length=32, blank=True)

  def __str__(self):
      return f"id={self.id}, user_id={self.user.id}, college={self.college}, major={self.major}"
  
  