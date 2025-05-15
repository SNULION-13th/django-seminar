from rest_framework import serializers

# 이게 있어야 swagger_ui를 적용 가능.

class AuthorRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class CommentCreateRequestSerializer(serializers.Serializer):
    author = AuthorRequestSerializer() # author는 따로 위에서 만든 authorserializer가 따로 불려온다.
    post = serializers.IntegerField()
    content = serializers.CharField()

class CommentUpdateRequestSerializer(serializers.Serializer):
    author = AuthorRequestSerializer()
    content = serializers.CharField()

class CommentDeleteRequestSerializer(serializers.Serializer):
    author = AuthorRequestSerializer()
