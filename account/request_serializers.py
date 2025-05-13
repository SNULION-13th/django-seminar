#request_serializers.py: 입력용 직렬화
'''
모델(db)과 연결되어 있지 않음
클라이언트가 보내는 데이터를 검증 & 처리하는 용도. 즉 유효성 검사만 진행함
'''


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