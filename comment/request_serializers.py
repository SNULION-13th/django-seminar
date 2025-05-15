from rest_framework import serializers
from account.request_serializers import SignInRequestSerializer

class CommentListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer(required=True)
    post = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)

class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer(required=True)
    content = serializers.CharField(required=True)