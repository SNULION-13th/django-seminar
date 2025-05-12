from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer

from post.models import Post

from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.models import User
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer

class CommentListView(APIView):

    ### 코멘트 생성하기.
    @swagger_auto_schema(
        operation_id="코멘트 생성",
        operation_description="게시글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 404: "Not Found", 400: "Bad Request", 403: "Forbidden",},
    )
    def post(self, request):
        try:
            post = Post.objects.get(id=request.data.get("post"))
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        content = request.data.get("content")
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
        if not content:
            return Response(
                {"detail": "[content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            comment = Comment.objects.create(post=post, content=content, author=author)
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="코멘트 목록 조회",
        operation_description="게시글에 대한 코멘트 목록을 조회합니다.",
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
        },
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id) # 실제 있는 포스트인지 확인용.
            comments = Comment.objects.filter(post=post_id)
        except:
            return Response(
                {"detail": "없는 포스트 번호입니닷!."}, status=status.HTTP_404_NOT_FOUND
            )
        
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CommentUpdateDeleteView(APIView):
    @swagger_auto_schema(
        operation_id="코멘트 수정",
        operation_description="코멘트를 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 404: "Not Found", 400: "Bad Request", 403: "Forbidden"},
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "[content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        comment.content = content


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



        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="코멘트 삭제",
        operation_description="코멘트를 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 403: "Forbidden"},
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
                status=status.HTTP_404_NOT_FOUND,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_404_NOT_FOUND,
            )
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
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

