from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from post.models import Post
from .serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.models import User
from account.request_serializers import SignInRequestSerializer


class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="댓글 목록을 조회합니다.",
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
        },
        manual_parameters=[
        openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="Post ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ]
    )
    def get(self, request): 
        post_id = request.GET.get("post")
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
    )
    def post(self, request):
        content = request.data.get("content")
        author = request.data.get("author")
        post = request.data.get("post")
        if not author:
            return Response(
                {"detail": "author field missing."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        username = author.get("username")
        password = author.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content:
            return Response(
                {"detail": "[content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not post:
            return Response(
                {"detail": "Post Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            post = Post.objects.get(id=post)
        except: 
            return Response(
                {"detail": "Post Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        comment = Comment.objects.create(content=content, author=author, post=post)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 403:"Forbidden", 404: "Not Found"},
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
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
                    status=status.HTTP_403_FORBIDDEN,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "[content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        comment.content = content
        comment.save()
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="댓글을 삭제합니다.",
    request_body=SignInRequestSerializer,
    responses={204: "No Content", 404: "Not Found", 400: "Bad Request", 401: "Unauthorized"},
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
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
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    