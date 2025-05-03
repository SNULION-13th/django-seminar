from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):
		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all() # Post를 다 가져와라
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        return Response({
            "id":post.id,
            "title":post.title,
            "content":post.content,
            "created_at":post.created_at
            }, status=status.HTTP_201_CREATED)
            # 이 return문에서 의문이 생겼다면 당신은 멋져요
            
class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
				### 수정 ###
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
				### 여기까지 ###

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)