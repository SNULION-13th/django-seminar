from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post, User, Comment

from .serializers import CommentSerializer
from .request_serializer import CommentRequestSerializer,CommentDetailRequestSerializer
from account.request_serializers import SignInRequestSerializer

# Create your views here.


class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="해당 게시글의 모든 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True), 404: "Not Found"},
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
        responses={201: CommentSerializer(many=True),400: "Bad Request",404: "Not Found", 403: "Forbidden"},
    )
    def post(self, request):
        post_id = request.data.get("post")
        content = request.data.get("content")
        author_info=request.data.get("author")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=400)

        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_404_NOT_FOUND
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
            operation_id="댓글 수정",
            operation_description="댓글을 수정합니다.",
            request_body=CommentDetailRequestSerializer,
            responses={
                200:CommentSerializer,
                400:"Bad Request",
                401:"Unauthorized",
                404:"Not found"
            }
    )


    def put(self, request, comment_id):
        try:
            comment=Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
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
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "[title, content] fields missing."},
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
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request",401:"Unauthorized"},
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
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
