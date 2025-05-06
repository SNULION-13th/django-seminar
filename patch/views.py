from django.shortcuts import render
# 수정
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import PatchPost
from .serializers import PatchSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class PostUpdateView(APIView):
  def patch(self, request, post_id):
    try:
      post = PatchPost.objects.get(id=post_id)
    except PatchPost.DoesNotExist:
      return Response({"error": "게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PatchSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)