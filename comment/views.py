from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.views import APIView
from post.models import Post
from rest_framework.response import Response
from account.models import User
from rest_framework import status
from.request_serializers import CommentCreateRequestSerializer
from.request_serializers import CommentUpdateRequestSerializer

from account.request_serializers import SignInRequestSerializer
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="Comment 목록 조회",
        operation_description="Comment 목록을 조회합니다.",
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found"
        },
    )
    def get(self, request):
        try:
            post_id = request.GET.get("postId")
            comments = Comment.objects.filter(post_id=post_id)
        except:
            return Response(
                {"detail": "Post Not Found."}, status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CommentCreateRequestSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="Comment 생성",
        operation_description="Comment를를 생성합니다.",
        request_body=CommentCreateRequestSerializer,
        responses={201: CommentSerializer,  400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
    )
    def post(self, request):
        author_info = request.data.get("author")
        post_id = request.data.get("post")

        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment_content = request.data.get("content")
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password or not comment_content:
            return Response(
                {"detail": "[username, password, post, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            comment = Comment.objects.create(
                post=post, content=comment_content, author=author
            )
        except :
            return Response(
                {"detail": "User Not Found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)    

class CommentDetailView(APIView):
    
    @swagger_auto_schema(
        operation_id="Comment 수정",
        operation_description="Comment를를 수정합니다.",
        request_body=CommentUpdateRequestSerializer,
        responses={200: CommentSerializer,  400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
    )
    def put(self, request, comment_id): 
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND,
            )
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        comment.content = content
        comment.save()
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="Comment 삭제",
        operation_description="Comment를 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."}
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
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
