from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from post.models import Post
from account.models import User
from .serializers import CommentSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.request_serializers import SignInRequestSerializer


class CommentListView(APIView):
	@swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="특정 게시글에 달린 댓글 목록을 조회합니다.",
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
        },
    )
	def get(self, request):
		try: 
			post = request.GET.get("post") # query parameter
			comments = Comment.objects.filter(post=post)
			comments_serializer = CommentSerializer(comments, many=True)
			return Response(comments_serializer.data, status=status.HTTP_200_OK)
		# wrong post id (404)
		except:
			return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

	# Comment Create
	@swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 
									 400: "Bad Request", 
									 403: "Forbidden",
									 404: "Not Found"},
    )
	def post(self, request):
		# post 지정 (404)
		try: 
			post_id = request.data.get("post")
			post = Post.objects.get(id=post_id)
		except:
			return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
		
		# author field 비어있는지 확인 (400)
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
		
		# author 지정 (404)
		try:
			author = User.objects.get(username=username)
			# 비밀번호 확인 (403)
			if not author.check_password(password):
					return Response(
							{"message": "Password is incorrect"},
							status=status.HTTP_403_FORBIDDEN,
					)
			# 사용자 확인된 경우 (201)
			content = request.data.get("content")
			comment = Comment.objects.create(post=post, content=content, author=author)
			comment_serializer = CommentSerializer(instance=comment)
			return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

		except User.DoesNotExist:
				return Response(
						{"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
				)
	

########################

	
class CommentDetailView(APIView):
	# Comment Update
	@swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        # request_body=CommentRequestserializer,
        responses={200: CommentSerializer,
									 400: "Bad Request", 
									 401: "Unauthorized",
									 403: "Forbidden",
									 404: "Not Found"},
    )
	def put(self, request, comment_id):
		try:
			comment = Comment.objects.get(id=comment_id)
		except: # no comment (404)
			return Response(
					{"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
			)
		
		author_info = request.data.get("author")
		if not author_info:
			return Response(
					{"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
			)
		username = author_info.get("username")
		password = author_info.get("password")
		if not username or not password:
			# missing field (400)
			return Response(
					{"detail": "[username, password] fields missing."},
					status=status.HTTP_400_BAD_REQUEST,
			)
		
		author = User.objects.get(username=username)
		if not author.check_password(password):
			# wrong password (403)
			return Response(
					{"message": "Password is incorrect."},
					status=status.HTTP_403_FORBIDDEN,
			)
		if comment.author != author:
			# no authorization of comment (401)
			return Response(
					{"message": "You are not the author of this post."},
					status=status.HTTP_401_UNAUTHORIZED,
			)
		
		content = request.data.get("content")
		if not content: # missing field (400)
			return Response(
				{"message": "[content] field missing."},
				status=status.HTTP_400_BAD_REQUEST
			)
		comment.content = content
		comment.save()
		comment_serializer = CommentSerializer(instance=comment)
		return Response(comment_serializer.data, status=status.HTTP_200_OK)

		
	# Comment Delete
	@swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 
									 400: "Bad Request",
									 401: "Unauthorized",
									 403: "Forbidden",
									 404: "Not Found"
									 },
    )
	def delete(self, request, comment_id):
		try:
			comment = Comment.objects.get(id=comment_id)
		except: # no comment (404)
			return Response(
					{"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
			)

		author_info = request.data.get("author")
		if not author_info:
			return Response(
					{"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
			)
		username = author_info.get("username")
		password = author_info.get("password")
		if not username or not password:
			# missing field (400)
			return Response(
					{"detail": "[username, password] fields missing."},
					status=status.HTTP_400_BAD_REQUEST,
			)
		
		author = User.objects.get(username=username)
		if not author.check_password(password):
			# wrong password (403)
			return Response(
					{"message": "Password is incorrect."},
					status=status.HTTP_403_FORBIDDEN,
			)
		if comment.author != author:
			# no authorization of comment (401)
			return Response(
					{"message": "You are not the author of this post."},
					status=status.HTTP_401_UNAUTHORIZED,
			)
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)