from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from post.models import Post
from .serializers import CommentSerializer
from account.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentList(APIView):

    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="post ID를 쿼리 파라미터로 받아 해당 게시글의 댓글 목록을 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='post',
                in_=openapi.IN_QUERY,
                description='댓글을 조회할 게시글의 ID',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
            400: "Bad Request",
        },
    )
    def get(self, request):
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


    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        }
    )
    def post(self, request):
        content = request.data.get("content")
        post_id = request.data.get("post")
        author_info = request.data.get("author")

        if not content or not post_id or not author_info:
            return Response(
                {"detail": "Missing one of required fields: content, post, author"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = author_info.get("username")
        password = author_info.get("password")

        if not username or not password:
            return Response(
                {"detail": "Missing author credentials (username/password)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        if not author.check_password(password):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(
            content=content,
            author=author,
            post=post
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
