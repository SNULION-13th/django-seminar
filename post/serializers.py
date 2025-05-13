from rest_framework.serializers import ModelSerializer, CharField
from tag.serializers import TagSerializer
from account.serializers import UserSerializer
from .models import Post, Comment

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    # Nested JSON is not needed
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id"]