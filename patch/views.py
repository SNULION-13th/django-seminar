from django.shortcuts import render
# 수정
from rest_framework.views import APIView
from .models import PatchPost
from .serializers import PatchSerializer

# Create your views here.
class PostUpdateView(APIView):
  queryset = PatchPost.objects.all()
  serializer_class = PatchSerializer
  lookup_field = 'id'
  