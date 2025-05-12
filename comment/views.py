from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from post.models import Post
from .serializers import CommentSerializer

# Create your views here.
def CommentList(request):
  post_id = request.GET.get('post')
  
  if not post_id:
    return Response({'error': 'post parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
  
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
  
  comments = Comment.objects.filter(post=post)
  serializer = CommentSerializer(comments, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)