from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import Comment
from post.models import Post
from account.models import User
from .serializers import CommentSerializer
from .request_serializers import CommentListRequestSerializer
from account.request_serializers import SignInRequestSerializer


class CommentListView(APIView):

    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="특정 댓글 목록을 조회합니다.",
        responses={
            200: CommentSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request):
        content = request.data.get("content")
        post_id = request.data.get("post")
        author_info = request.data.get("author")

        if not content or not post_id or not author_info:
            return Response(
                {"detail": "Missing required fields [content, post, author]"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = author_info.get("username")
        password = author_info.get("password")

        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        comment = Comment.objects.create(
            content=content,
            post=post,
            author=author
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다",
        request_body=CommentDetailRequestSerializer,
        responses={
            200:CommentSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing"},
                status=status.HTTP_400_BAD_REQEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        
        try:
            author = User.objects.get(username=username)
            if not author.ckeck_password(password):
                return Response(
                    {"detail": "You are not the author of this comment"},
                    status=status.HTPP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "[content] field missins"},
                status=status.HTTP_400_BAD_REQEST,
            )
        comment.content = content
        comment.save()

        serializer=CommentSerializer(isinstance=comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
      operation_id="댓글 삭제",
      operation_description="댓글을 삭제합니다",
      request_body=SignInRequestSerializer,
      responses={
          204: "No Content",
          400: "Bad Request",
          401: "Unauthorized",
          403: "Forbidden",
          404: "Not Found",
      },
  )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
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
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
