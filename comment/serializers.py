from rest_framework.serializers import ModelSerializer
from .models import Comment
from post.serializers import PostSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        