from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    id         = serializers.IntegerField(read_only=True)
    content    = serializers.CharField(min_length=1)
    created_at = serializers.DateTimeField(read_only=True)
    post       = serializers.IntegerField(source='post.id', read_only=True)
    author     = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'content', 'created_at', 'post', 'author']
