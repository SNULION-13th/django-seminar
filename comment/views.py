from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from post.models import Post
from .serializers import CommentSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.models import User
from account.request_serializers import SignInRequestSerializer
## 쿼리파라미터를 위한 import
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="댓글 목록을 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                name="post",
                in_=openapi.IN_QUERY,
                description="댓글을 조회할 Post의 ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found", ## wrong post id
        },
    )
    def get(self, request):
      ## 쿼리 파라미터 쓰는 방법은 gpt가 알려줬습니다...
        # 1) 쿼리 파라미터에서 post ID 꺼내기
        post_id = request.GET.get('post')
        # 2) Post 객체 존재 확인 (없으면 404)
        post_obj = get_object_or_404(Post, pk=post_id)
        # 3) 해당 Post의 댓글만 필터링
        comments = Comment.objects.filter(post=post_obj)       
        # 4) 직렬화 후 응답
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request", ## missing field
            403: "Forbidden", ## password 불일치
            404: "Not Found", ## author or post not found
        },
    )
    def post(self, request):
      author_info = request.data.get("author")
      content = request.data.get("content")
      post_id = request.data.get("post")
      if not post_id:
          return Response(
              {"detail": "post field missing."},
              status=status.HTTP_400_BAD_REQUEST,
          )
      post_obj = get_object_or_404(Post, pk=post_id)
      if not author_info:
          return Response(
              {"detail": "author field missing."}, 
              status=status.HTTP_400_BAD_REQUEST
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
              {"detail": "content field missing."},
              status=status.HTTP_400_BAD_REQUEST,
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

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={
            200: CommentSerializer,
            404: "Not Found", ## author or comment not found
            400: "Bad Request", ## missing field
            403: "Forbidden", ## password 불일치 / no authorization of comment
        },
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."},
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
                {"detail": "User Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        comment.content = content
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={
            204: "No Content",
            404: "Not Found",
            400: "Bad Request",
            401: "Unauthorized",
        },
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."},
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
                {"detail": "User Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)