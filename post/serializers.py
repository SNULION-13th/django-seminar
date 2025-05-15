from rest_framework.serializers import ModelSerializer
from .models import Post
from tag.serializers import TagSerializer
from comment.serializers import CommentSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ## comment 추가
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"