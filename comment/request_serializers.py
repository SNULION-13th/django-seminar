from rest_framework import serializers
from account.request_serializers import SignInRequestSerializer

class CommentCreateRequestSerializer(serializers.Serializer):
  author = SignInRequestSerializer()
  post = serializers.IntegerField()
  content = serializers.CharField()

class CommentUpdateRequestSerializer(serializers.Serializer):
  author = SignInRequestSerializer()
  content = serializers.CharField()