from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.request_serializers import SignInRequestSerializer


from post.models import Post
from post.serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema
from account.models import User
from drf_yasg import openapi


class CommentListView(APIView):
  @swagger_auto_schema(
    operation_id='포스트의 댓글 목록 조회',
    operation_description='댓글 목록을 조회합니다.',
    manual_parameters=[
            openapi.Parameter(
                'post',  # 쿼리 파라미터 이름
                openapi.IN_QUERY,  # 쿼리스트링에서 받음
                description='조회할 포스트의 ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    responses={200: CommentSerializer(many=True), 404: "Not Found"},
  )
  def get(self, request):
    post_id = request.query_params.get("post")
    try:
      post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
      return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(post.comments.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
    operation_id='댓글 생성',
    operation_description='댓글을 생성합니다.',
    request_body=CommentListRequestSerializer,
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
  )
  def post(self, request):
    author_info = request.data.get("author")
    post_id = request.data.get("post")
    content = request.data.get("content")

    if not author_info:
      return Response({"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST)
  
    username = author_info.get("username")
    password = author_info.get("password")
    if not username or not password:
      return Response({"detail": "[username, password] fields missing in author"}, status=status.HTTP_400_BAD_REQUEST)

    if not content:
      return Response({"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response({"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
      
      comment = Comment.objects.create(
        post=Post.objects.get(id=post_id),
        content=content,
        author=author
      )
    except Post.DoesNotExist:
      return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
      return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except:
      return Response({"detail": "Error occurred."}, status=status.HTTP_400_BAD_REQUEST)
  
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  

class CommentDetailView(APIView):
  @swagger_auto_schema(
    operation_id='댓글 수정',
    operation_description='댓글을 수정합니다.',
    request_body=CommentDetailRequestSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
  )
  def put(self, request, comment_id):
    author_info = request.data.get("author")
    content = request.data.get("content")

    if not author_info:
      return Response({"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST)
    
    username = author_info.get("username")
    password = author_info.get("password")
    if not username or not password:
      return Response({"detail": "[username, password] fields missing in author"}, status=status.HTTP_400_BAD_REQUEST)

    if not content:
      return Response({"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response({"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
      
      comment = Comment.objects.get(id=comment_id)
      if comment.author != author:
        return Response({"detail": "You are not the author of this comment."}, status=status.HTTP_403_FORBIDDEN)

      comment.content = content
      comment.save()
    except Comment.DoesNotExist:
      return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
      return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except:
      return Response({"detail": "Error occurred."}, status=status.HTTP_400_BAD_REQUEST)
  
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
    operation_id='댓글 삭제',
    operation_description='댓글을 삭제합니다.',
    request_body=SignInRequestSerializer,
    responses={204: "No Content", 403: "Forbidden", 404: "Not Found"}
  )
  def delete(self, request, comment_id):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
      return Response({"detail": "[username, password] fields missing in author"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response({"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
      
      comment = Comment.objects.get(id=comment_id)
      if comment.author != author:
        return Response({"detail": "You are not the author of this comment."}, status=status.HTTP_403_FORBIDDEN)

      comment.delete()
    except Comment.DoesNotExist:
      return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
      return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except:
      return Response({"detail": "Error occurred."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)
    
  