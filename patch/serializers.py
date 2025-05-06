from rest_framework.serializers import ModelSerializer
from .models import PatchPost

class PatchSerializer(ModelSerializer):
    class Meta:
        model = PatchPost
        fields = "__all__"