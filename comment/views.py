from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer
from .request_serializers import CommentRequestSerializer
from post.models import Post
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Comment


class CommentView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 생성",
    operation_description="댓글을 생성합니다.",
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
  )
  
  def post(self, request):
    author_data = request.data.get("author")
    post_id = request.data.get("post")
    content = request.data.get("content")

    if not author_data or not post_id or not content:
      return Response({"detail": "missing field in request"}, status=400)
    
    username = author_data.get("username")
    password = author_data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
      return Response({"detail": "User not found"}, status=404)
    
    post = get_object_or_404(Post, id=post_id)

    if not user.check_password(password):
      return Response({"detail": "Password is incorrect."}, status=403)
    
    serializer = CommentSerializer(data={
      "author": user.id,
      "post": post.id,
      "content": content
      })

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    else:
      return Response(serializer.errors, status=400)
  
  @swagger_auto_schema(
    operation_id='댓글 목록 조회',
    operation_description='댓글 목록을 조회합니다.',
    manual_parameters=[
            openapi.Parameter(
                'post',
                openapi.IN_QUERY,
                description="댓글을 조회할 게시글의 ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
    responses={200: CommentSerializer(many=True), 404: "Not found"}
  )
  def get(self, request):
    comments = Comment.objects.all()
    post_id= request.GET.get("post")
    if not post_id:
      return Response({"detail": "Post not found"}, status=404)
    
    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(instance=comments, many=True)
    return Response(serializer.data, status=200)


class CommentDetailView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="댓글을 삭제합니다.",
    request_body=CommentRequestSerializer,
    responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
    )
  def delete(self, request, comment_id):
    try: 
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response(
        {"detail": "Comment Not found."}, status=404)

    author_data = request.data
    if not author_data:
      return Response(
                {"detail": "author field missing."},
                status=400,
            )
    username = author_data.get("username")
    password = author_data.get("password")
    if not username or not password:
      return Response(
        {"detail": "[username, password] fields missing."},
          status=400,
            )
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response(
          {"detail": "Password is incorrect."},
            status=403,
            )
      if comment.author != author:
        return Response(
          {"detail": "You are not the author of this post."},
            status=403,
            )
    except:
      return Response(
         {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
          )
    
    comment.delete()
    return Response(status=204)
  
  @swagger_auto_schema(
    operation_id="게시글 수정",
    operation_description="게시글을 수정합니다.",
    request_body=CommentRequestSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
    )
  def put(self, request, comment_id):
      try:
          comment = Comment.objects.get(id=comment_id)
      except:
        return Response(
          {"detail": "Comment not found."}, status=404
          )

      author_data = request.data.get("author")
      if not author_data:
        return Response(
          {"detail": "author field missing."}, status=400
          )
      username = author_data.get("username")
      password = author_data.get("password")
      try:
        author = User.objects.get(username=username)
        if not author.check_password(password):
          return Response(
            {"detail": "Password is incorrect."},
              status=403,
              )
        if comment.author != author:
          return Response(
            {"detail": "You are not the author of this comment."},
              status=403,
              )
      except:
        return Response(
          {"detail": "User not found."}, status=404
          )

      content = request.data.get("content")
      if not content:
       return Response({"detail": "content field missing."}, status=400)

      comment.content = content
      comment.save()

      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=200)
