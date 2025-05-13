from rest_framework import serializers
from account.request_serializers import SignInRequestSerializer

class CommentDetailRequest(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    
class CommentRequestSerializer(serializers.Serializer):
  content = serializers.CharField()
  user =CommentDetailRequest()
  post = serializers.IntegerField()

class CommentUpdateSerializer(serializers.Serializer):
  user =CommentDetailRequest()
  content = serializers.CharField()