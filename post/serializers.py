from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"