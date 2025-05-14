# comment/request_serializers.py

from rest_framework import serializers

class CommentSignInRequestSerializer(serializers.Serializer):
    """공통 인증용 시리얼라이저 (DELETE, 기타 auth)"""
    email    = serializers.EmailField(label="Email",    min_length=1)
    username = serializers.CharField(   label="Username", min_length=1)
    password = serializers.CharField(   label="Password", min_length=1)


    class Meta:
        ref_name = "CommentSignInRequest"


class CommentCreateRequestSerializer(serializers.Serializer):
    author  = CommentSignInRequestSerializer(label="Author")
    post    = serializers.IntegerField(label="Post")
    content = serializers.CharField(label="Content", min_length=1)

    class Meta:
        ref_name = "CommentCreateRequest"


class CommentUpdateRequestSerializer(serializers.Serializer):
    author  = CommentSignInRequestSerializer(label="Author")
    content = serializers.CharField(label="Content", min_length=1)

    class Meta:
        ref_name = "CommentUpdateRequest"


class CommentDeleteRequestSerializer(serializers.Serializer):
    """삭제 전용 인증 시리얼라이저"""
    email    = serializers.EmailField(label="Email",    min_length=1)
    username = serializers.CharField(   label="Username", min_length=1)
    password = serializers.CharField(   label="Password", min_length=1)

    class Meta:
        ref_name = "CommentDeleteRequest"
