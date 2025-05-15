from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "author": {"allow_null": False},  ## swagger에서 author가 x-nullable: true로 나와서
        }