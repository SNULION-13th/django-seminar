from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer
from post.serializers import PostSerializer
from .models import Comment

class CommentRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    post = serializers.IntegerField()
    content = serializers.CharField()


class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()