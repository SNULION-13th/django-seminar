from django.shortcuts import render

# Create your views here.

# Comment는 Tag 같은거와 달리 완전 독립적인 CRUD를 만드는 느낌임.
# 그래서 Tag 보다는 오히려 Post의 views와 닮은 느낌.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from post.models import Post
from .models import Comment
from .serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from comment.request_serializers import (
    CommentCreateRequestSerializer,
    CommentUpdateRequestSerializer,
    CommentDeleteRequestSerializer,
)
from drf_yasg import openapi

class CommentView(APIView):
    @swagger_auto_schema(
    operation_id="댓글 목록 조회",
    operation_description="쿼리 파라미터로 post ID를 받아 해당 게시글의 모든 댓글을 조회합니다.",
    manual_parameters=[ # 이거 추가해야지 쿼리 파라미터가 가능하단다.
        openapi.Parameter(
            name='post',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='댓글을 조회할 대상 게시글의 ID'
        )
    ],
    responses={200: CommentSerializer(many=True), 404: "Not Found"},
)
    def get(self, request): # 특정 게시물 comment 다 불러오기
        post_id = request.query_params.get('post') # 쿼리 파라미터를 이용하는. 쿼리 파라미터에 무슨 값이 있는지 꺼내온다.
        try:
            post = Post.objects.get(id=post_id) # 해당 post를 가져오려고 해보고, 만약 없으면 404 반환.
        except Post.DoesNotExist:
            return Response({"error": "post not found"}, status=404)

        comments = Comment.objects.filter(post=post) # 해당 post id에 해당하는 모든 comment들을 가져와서
        serializer = CommentSerializer(comments, many=True) # 형식에 맞춰주고
        return Response(serializer.data, status=200) # 보낸다.
    
    
    @swagger_auto_schema(
    operation_id="댓글 생성",
    operation_description="게시글 ID와 작성자 정보 및 내용을 입력받아 댓글을 생성합니다.",
    request_body=CommentCreateRequestSerializer,
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
)
    def post(self, request):  # comment create(id 자동 부여)
        data = request.data # 요청과 함께 보낸 body를 가져와서
        required_fields = ['post', 'content', 'author'] # 일단 큰 구조를 한번 쭉 검사하고
        if not all(field in data for field in required_fields):
            return Response({"error": "missing field"}, status=400)
          
        # author안에 올바른 로그인 정보있는지 다시 확인.
        author_data = data['author']
        required_author_fields = ['email', 'username', 'password'] # 이렇게 세 구조가 있어야한다.
        if not all(field in author_data for field in required_author_fields):
            return Response({"error": "missing author field"}, status=400) 

        try:
            post = Post.objects.get(id=data['post'])
        except Post.DoesNotExist:
            return Response({"error": "post not found"}, status=404) # 해당 post가 없으면 404


        try:
            author = User.objects.get(email=author_data['email'], username=author_data['username']) 
            # 이런 user가 있는지를 검색해서 author에 저장.
        except User.DoesNotExist:
            return Response({"error": "author not found"}, status=404)

        if not author.check_password(author_data['password']): # author 있긴 있는데 비번 틀렸으면 403 / check_password는 내장함수
            return Response({"error": "password wrong"}, status=403)

        # 지금까지 다 통과했으면 드디어 comment 만들기.
        comment = Comment.objects.create(post=post, author=author, content=data['content']) # 만든시간은 자동으로 들어감. 앞에서 설정한번 해줬어서.
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=201)


class CommentDetailView(APIView):
  
    @swagger_auto_schema(
    operation_id="댓글 수정",
    operation_description="작성자 인증 정보를 포함하여 댓글 내용을 수정합니다. 본인만 수정 가능.",
    request_body=CommentUpdateRequestSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 403: "Unauthorized", 404: "Not Found"}
)
    def put(self, request, comment_id): # 특정 comment 업데이트. 권한 있을때만 업뎃 가능 
        data = request.data
        
        # post랑 느낌 매우 비슷하다. comment의 content 접근하고, 정보 업데이트만 나중에 가져오면 됨.
        
        
        required_fields = ['author', 'content']
        if not all(field in data for field in required_fields):
            return Response({"error": "missing field"}, status=400) # 큰거에서 먼저 찾아보고
          
        author_data = data['author'] # 작은거에서도 찾아보고.
        required_author_fields = ['email', 'username', 'password']
        if not all(field in author_data for field in required_author_fields):
            return Response({"error": "missing author field"}, status=400)

        try:
            comment = Comment.objects.get(id=comment_id) # comment가 존재하는지 여부 따지기.
        except (Comment.DoesNotExist, User.DoesNotExist):
            return Response({"error": "author or comment not found"}, status=404)

          
        try:
            author = User.objects.get(email=author_data['email'], username=author_data['username'])
        except User.DoesNotExist:
            return Response({"error": "author not found"}, status=404) # 똑같은 방식으로 author도 있는지 따지기.

            # 5. 비밀번호 확인 / 비번 틀렸으면 403!
        if not author.check_password(author_data['password']):
            return Response({"error": "password wrong"}, status=403)
      
        if comment.author != author:
            return Response({"error": "no authorization of comment"}, status=403) # 지금 로그인한게 원래 author인지 확인하기.

        comment.content = data['content'] # 모두 다 통과했으면 content에 접근해서 수정하고 save하기!
        comment.save()
        return Response(CommentSerializer(comment).data, status=200)


    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="작성자 인증 정보를 포함하여 댓글을 삭제합니다. 본인만 삭제 가능.",
        request_body=CommentDeleteRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            403: "Unauthorized",
            404: "Not Found"
        },
    )
    def delete(self, request, comment_id):  # 특정 comment 삭제. 마찬가지로 권한 있을때만 삭제 가능.
        data = request.data

        # 앞이랑 똑같은거 또 반복.

        if 'author' not in data:
            return Response({"error": "missing field: author"}, status=400)

        author_data = data['author']
        required_fields = ['email', 'username', 'password']
        if not all(field in author_data for field in required_fields):
            return Response({"error": "missing field in author"}, status=400)

        # 유효한 사용자인지 확인
        try:
            author = User.objects.get(email=author_data['email'], username=author_data['username'])
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)

        # 비밀번호 유효한지 확인.
        if not author.check_password(author_data['password']):
            return Response({"error": "unauthorized"}, status=403) # 이때도 403

        # 코멘트 존재 여부 확인ㄴ 
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "comment not found"}, status=404)

        # 권한 있는지 확인
        if comment.author != author:
            return Response({"error": "forbidden: not the comment owner"}, status=403)

        # 다 했으면 삭제!
        comment.delete()
        return Response(status=204)
