from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
#### 수정 ###
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#### 여기까지 ###

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
#### 수정 ###
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

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
    


    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # 기존 인스턴스와 요청 데이터를 바탕으로 시리얼라이저 생성
        serializer = PostSerializer(post, data=request.data, partial=True)  # partial=True이면 일부만 수정 가능

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)