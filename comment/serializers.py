from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerializer(ModelSerializer): # 데이터 형식 정해주기. 이런 데이터들이 Comment에 존재한다.
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
