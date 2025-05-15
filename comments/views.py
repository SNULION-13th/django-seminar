from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post, User, Comment

from post.serializers import PostSerializer
from .serializers import CommentSerializer
from .request_serializer import CommentRequestSerializer
#from account.request_serializers import SignInRequestSerializer
#from post.request_serializers import PostDetailRequestSerializer

# Create your views here.


class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="해당 게시글의 모든 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True),404: "Wrong post id", 400: "Bad Request"},
    )
    def get(self, request):
        post_id=request.GET.get("post")

        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)

        return  Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="해당 게시글에 댓글을 작성합니다.",
        request_body=CommentRequestSerializer,
        responses={200: CommentSerializer(many=True),404: "Wrong post id", 400: "Bad Request"},
    )
    def post(self, request):
        post_id = request.data.get("post")
        content = request.data.get("content")
        author_info=request.data.get("author")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=404)

        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        if not username :
            return Response(
                {"detail": "[username] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content:
            return Response(
                {"detail": "[content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            author = User.objects.get(username=username)
            comment = Comment.objects.create(content=content, author=author,post=post)
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



















    @swagger_auto_schema(
        operation_id="게시글 삭제",
        operation_description="게시글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request"},
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )

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

    @swagger_auto_schema(
        operation_id="게시글 수정",
        operation_description="게시글을 수정합니다.",
        request_body=PostDetailRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

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

        title = request.data.get("title")
        content = request.data.get("content")
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
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)