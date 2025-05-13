#serilaizers.py: 출력용 직렬화

from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
#class Meta: 어떤 모델에 대해서, 그 모델의 어떤 필드들을 serialize하는 대상으로 할 것인지 설정

#User모델의 일부 필드만 골라 직렬화
class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

#User모델의 모든 필드를 직렬화
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]


class UserProfileSerializer(ModelSerializer):
    #UserProfile모델에 이미 user필드 존재
    # !!!user필드에 오버라이딩 (foriegnKey인 user를 단순히 숫자 id로 출력하지 않고, serialize를 완료한 형태로 출력하겠다는 의미)
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = "__all__" 