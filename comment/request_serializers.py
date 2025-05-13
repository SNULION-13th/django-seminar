from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer

class CommentListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())