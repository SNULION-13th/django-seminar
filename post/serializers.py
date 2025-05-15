from rest_framework.serializers import ModelSerializer
from .models import Post,Like
from tag.serializers import TagSerializer
from comments.serializers import CommentSerializer
from account.serializers import UserIdUsernameSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(ModelSerializer):
    user = UserIdUsernameSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ["user","post","created_at"]

