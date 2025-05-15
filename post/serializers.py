from rest_framework.serializers import ModelSerializer

from tag.serializers import TagSerializer

from .models import Post

class PostSerializer(ModelSerializer):
    
    tags = TagSerializer(many=True, read_only=True) # tag가 여러개 달려있을 수도 있으니까 many = True로.
    
    class Meta:
        model = Post
        fields = "__all__"