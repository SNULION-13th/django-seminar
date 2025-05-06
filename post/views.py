from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema


class PostListView(APIView):
		### 얘네가 class inner function 들! ###
    
    @swagger_auto_schema(  ## 함수 설명해주는 데코레이터. swagger api 문서화에 사용된다~
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={200: PostSerializer(many=True)}
        )
    def get(self, request): 
        posts = Post.objects.all() # 존재하는 Post들을 전부 다 가져와라
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer}
        ) # 함수 설명해주는 데코레이터
    def post(self, request): # 얘는 request data가 있다. body에 title, content를 같이 보내기 때문에.
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content) # 딱 하나의 post를 생성하겠다.
        serializer = PostSerializer(post) # 틀을 만들어주고 아래에서 그냥 .data로 꺼내주는.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 이 return문에서 의문이 생겼다면 당신은 멋져요
            
            
            
class PostDetailView(APIView):

    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            responses={200: PostSerializer}
        )
    def get(self, request, post_id): # get은 request 안쓴다. 그래서 회색빛.
        try:
            post = Post.objects.get(id=post_id) # 앞에와는 다르게 딱 하나만을 id를 이용해서 가져온다.
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
            operation_id='게시글 삭제',
            operation_description='게시글을 삭제합니다.',
            responses={204: 'No Content', 404: 'Not Found'}
        )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    ## 이후에 세부 게시물에 대해서 수정하는 기능 추가해야. -> PUT!
    ## 그리고 이건 사실상 id 매개변수가 들어있는 post 느낌이겠지. 그냥 get + post라고 생각하면 될듯.
    @swagger_auto_schema( # 데코레이터는 request 있는 post와 비슷하게.
            operation_id='게시글 수정',
            operation_description='게시글을 수정합니다.',
            request_body=PostSerializer, # request body의 '구조'를 설명하는.
            responses={200: PostSerializer, 404: 'Not Found', 400: 'Bad Request'}
        )
    def put(self, request, post_id):
        # 먼저 get_id와 비슷하게 하고.
        try: 
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 이 post에 들어있는 title과 content를 request의 title과 content로 바꿔준다. 
        
        
        title = request.data.get('title')
        content = request.data.get('content')
        
        # 예외처리 한번
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        post.title = title
        post.content = content
        # 이러면 post에 들어있는 title과 content가 request의 title과 content로 바뀌었다.
        
        post.save() # 이게 꼭 필요하대. 없으면 db에 반영이 안된대. 안하면 단순히 post의 변수만 바뀌는 느낌.
        
        # 마지막 리턴문.
        serializer = PostSerializer(post) 
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
        
        