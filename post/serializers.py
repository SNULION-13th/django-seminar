from rest_framework.serializers import ModelSerializer
### 🔻 이 부분 추가 🔻 ###
from tag.serializers import TagSerializer
### 🔺 이 부분 추가 🔺 ###
from .models import Post

class PostSerializer(ModelSerializer):
		### 🔻 이 부분 추가 🔻 ###
    tags = TagSerializer(many=True, read_only=True)
		### 🔺 이 부분 추가 🔺 ###
    class Meta:
        model = Post
        fields = "__all__"
