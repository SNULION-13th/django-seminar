from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerializer(ModelSerializer):
  class Mate:
    model = Comment
    fields = "__all__"