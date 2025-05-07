from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer): # 미리 구현된 ModelSerializer를 상속받아 PostSerializer를 구현
    # ModelSerializer는 Model을 기반으로 Serializer를 만들어주는 역할을 한다.
    class Meta:
        model = Post
        fields = "__all__"