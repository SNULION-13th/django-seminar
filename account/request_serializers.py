### 🔻 이 부분 추가 🔻 ###
from rest_framework import serializers


class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    college = serializers.CharField()
    major = serializers.CharField()

    class Meta:
            ref_name = "AccountSignUpRequest"
class SignInRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        ref_name = "AccountSignInRequest"

### 🔺 이 부분 추가 🔺 ###