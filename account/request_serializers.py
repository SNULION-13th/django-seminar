#편의를 위해서 serializer과 request_serializer를 나눔
#serializer: 출력
#request_serializer: 유저의 요청을 위해 사용되는 클래스들
### 🔻 이 부분 추가 🔻 ###
from rest_framework import serializers


class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    college = serializers.CharField()
    major = serializers.CharField()


class SignInRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

### 🔺 이 부분 추가 🔺 ###