from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post, Comment

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'post']