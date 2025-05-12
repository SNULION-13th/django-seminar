from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from post.serializers import PostSerializer
from post.models import Post
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .request_serializers import (
    CommentListRequestSerializer,
    CommentDetailRequestSerializer,
)
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .models import Comment
from drf_yasg import openapi


# Create your views here.
class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="post_id에 대한 댓글을 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                "post",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: CommentSerializer(many=True), 404: "Not Found"},
    )
    def get(self, request):
        try:
            post_id = request.GET.get("post")
            posts = Post.objects.filter(id=post_id)
            comments = Comment.objects.filter(post__in=posts)
            return Response(
                CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK
            )
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id="댓글 추가",
        operation_description="댓글을 추가합니다.",
        request_body=CommentListRequestSerializer,
        responses={
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            201: CommentSerializer,
        },
    )
    def post(self, request):
        post_id = request.data.get("post_id")
        content = request.data.get("content")
        author_info = request.data.get("author")
        if not post_id or not content or not author_info:
            return Response(
                {"detail": "[post_id, content, author] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check user
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_404_NOT_FOUND,
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
            post = Post.objects.get(id=post_id)
            if not post:
                return Response(
                    {"detail": "Post not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            comment = Comment.objects.create(content=content, author=author, post=post)
        except:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="comment_id에 대한 댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            author_info = request.data.get("author")
            if not author_info or not comment_id:
                return Response(
                    {"detail": "field missing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            username = author_info.get("username")
            password = author_info.get("password")
            author = User.objects.get(username=username)
            if not author:
                return Response(
                    {"detail": "Author not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if not comment:
                return Response(
                    {"detail": "Comment not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            content = request.data.get("content")
            updated_comment = Comment.objects.filter(id=comment_id).update(
                content=content
            )
            comment = Comment.objects.get(id=comment_id)

            return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="comment_id에 대한 댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            if not comment_id:
                return Response(
                    {"detail": "field missing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            username = request.data.get("username")
            password = request.data.get("password")
            author = User.objects.get(username=username)
            if not author:
                return Response(
                    {"detail": "Author not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if not comment:
                return Response(
                    {"detail": "Comment not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            updated_comment = Comment.objects.filter(id=comment_id).delete()

            return Response({"detail": "No content"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
