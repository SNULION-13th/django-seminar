from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post,Like
from .serializers import PostSerializer
from .request_serializers import PostListRequestSerializer, PostDetailRequestSerializer
# swagger 임포트
from drf_yasg.utils import swagger_auto_schema

### 🔻 이 부분 추가 🔻 ###
from .request_serializers import PostListRequestSerializer
### 🔺 이 부분 추가 🔺 ###
...

### 🔻 이 부분 수정 🔻 ###
from account.models import User
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer
### 🔺 이 부분 수정 🔺 ###

class PostListView(APIView):
    ## 여길 추가합니다-------
    @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={
                200: PostSerializer(many=True),
                404: "Not Found",
                400: "Bad Request",
            },
        )
    ## ----------------------------
		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all() # Post를 다 가져와라
        #### 수정 ###
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #### 여기까지 ###
     ## 여길 추가합니다-------
    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostListRequestSerializer,
            responses={201: PostSerializer, 404: "Not Found", 400: "Bad Request"},
        )
    ## ----------------------------   

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        tag_contents = request.data.get('tags')
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post = Post.objects.create(title=title, content=content, author=author)
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if tag_contents is not None:
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #### 여기까지 ###
            
class PostDetailView(APIView):
    ## 요기요기
    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            responses={200: PostSerializer}
        )
    ## 요기요기
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        ### 수정 ###
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
				### 여기까지 ###
    ## 요기요기
    @swagger_auto_schema(
            operation_id='게시글 삭제',
            operation_description='게시글을 삭제합니다.',
            responses={204: 'No Content', 404: 'Not Found'}
        )
    ## 요기요기   
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    ##과제!
    @swagger_auto_schema(
            operation_id='게시글 수정',
            operation_description='게시글의 제목과 내용을 수정합니다.',
            responses={200: PostSerializer, 404: 'Not Found'}
        )
    def put(self,request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        title =  request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.title = title
        post.content = content
        tag_contents = request.data.get("tags")
        if tag_contents is not None:
            post.tags.clear()
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        post.save() 
        
        serializer = PostSerializer(post)
                
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LikeView(APIView):
    @swagger_auto_schema(
        operation_id="좋아요 토글",
        operation_description="좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.",
        request_body=SignInRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request, post_id):

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ### 2 ###
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        ### 3 ###
        is_liked = post.like_set.filter(user=author).count() > 0

        ### 4 ###
        if is_liked == True:
            post.like_set.get(user=author).delete()
            print("좋아요 취소")
        else:
            Like.objects.create(user=author, post=post)
            print("좋아요 누름")

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)