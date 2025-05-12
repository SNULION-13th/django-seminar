from rest_framework import serializers
from account.request_serializers import SignInRequestSerializer


class CommentListRequestSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    content = serializers.CharField()
    author = SignInRequestSerializer()


class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()
