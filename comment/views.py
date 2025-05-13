from django.shortcuts import render

from django.contrib import auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Comment
from post.models import Post
from django.contrib.auth.models import User
from account.request_serializers import SignInRequestSerializer

from .request_serializers import CommentRequestSerializer, CommentUpdateSerializer
from .serializers import CommentViewSerializer
# Create your views here.

class CommentList(APIView):
  @swagger_auto_schema(
        operation_id="댓글 목록 보기",
        operation_description="query parameter로 post id를 넘겨주면 해당 post의 모든 comments를 리턴",
        responses={200: CommentViewSerializer(many = True), 404: "post not found"},
    )
  def get(self,request):
    try:
      post_id = int(request.GET.get("post"))
    except (TypeError, ValueError):
      return Response({"message": "Missing 'post' query parameter"}, status=400)
    comments = Comment.objects.filter(post_id=post_id) 
    serializer = CommentViewSerializer(comments, many = True )
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class CommentCreate(APIView):
  @swagger_auto_schema(
        operation_id="댓글 생성하기",
        operation_description="댓글 생성",
        request_body = CommentRequestSerializer,
        responses={201: CommentViewSerializer  , 404: "post or author not found", 400: 'missing field in request', 403: 'password wrong'},
    )
  def post(self, request):
    serializer = CommentRequestSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    
    author_email =  serializer.validated_data['user']['email']
    post_id = serializer.validated_data['post']
    content = serializer.validated_data['content']

    try:
        user = User.objects.get(email = author_email )
    except User.DoesNotExist:
        return Response({"message": "Author not found"}, status=404)
    
    try:
      post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
      return Response({"message": "Post not found"}, status=404)
    
    password = request.data.get("password")
    if password is None:
      return Response({"message":"Missing password"},status=400)
    if not user.check_password(password):
      return Response({"message":"Password is incorrect"},status = 403)
    
    # 댓글 생성
    comment = Comment.objects.create(
      content=content,
      author=user,
      post=post
    )

    # 응답 직렬화
    response_serializer = CommentViewSerializer(comment)
    return Response(response_serializer.data, status=201)
  
class CommentUpdate(APIView):
  @swagger_auto_schema(
      operation_id="댓글 수정하기",
      operation_description="댓글 수정",
      request_body =CommentUpdateSerializer,
      responses={201: CommentViewSerializer, 400: "missing field", 403: "password 불일치", 404: "post or author not found"},
    )
  def put(self,request, commentId):
    serializer = CommentUpdateSerializer(data = request.data)
    if not serializer.is_valid():
      return Response({'message':"missing field"},status=400)
    
    try:
      comment = Comment.objects.get(id = commentId)
      author = comment.author
    except (Comment.DoesNotExist):
      return Response({'message':"comment or Author notfound"},status = 404)
    
    password = request.data.get("user",{}).get("password")
    if not author.check_password(password):
      return Response({"message":"Password is incorrect"},status = 403)
    
    #user는 dict이고 author은 User객체이기 때문에 직접 비교할 수 없음
    request_email = serializer.validated_data['user']['email']
    if request_email != author.email:
      return Response({"message":"No authorization"} , status = 403)
    
    content = serializer.validated_data['content']
    comment.content = content
    comment.save()
    return Response(CommentViewSerializer(comment), status =200)
  
  @swagger_auto_schema(
        operation_id="댓글 삭제하기",
        operation_description="로그인된 사용자가 자신이 작성한 댓글을 삭제합니다.",
        responses={
            204: "정상 삭제",
            403: "비밀번호 불일치 또는 권한 없음",
            404: "댓글 없음",
        },
  )
  def delete(self, request, commentId):
    try:
        comment = Comment.objects.get(id=commentId)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=404)

    if comment.author != request.user:
        return Response({"message": "No authorization"}, status=403)

    comment.delete()
    return Response(status=204)
    
    
        
    