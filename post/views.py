from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from account.models import User
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer
from .request_serializers import PostListRequestSerializer, PostDetailRequestSerializer, CommentRequestSerializer, CommentDetailRequestSerializer
from drf_yasg import openapi


class PostListView(APIView):
    @swagger_auto_schema(
        operation_id="게시글 목록 조회",
        operation_description="게시글 목록을 조회합니다.",
        responses={
            200: PostSerializer(many=True),
            404: "Not Found",
            400: "Bad Request",
        },
    )
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="게시글 생성",
        operation_description="게시글을 생성합니다.",
        request_body=PostListRequestSerializer,
        responses={201: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        tag_contents = request.data.get("tags")
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
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post = Post.objects.create(title=title, content=content, author=author)
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if tag_contents is not None:
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostDetailView(APIView):
    @swagger_auto_schema(
        operation_id="게시글 상세 조회",
        operation_description="게시글 1개의 상세 정보를 조회합니다.",
        responses={200: PostSerializer, 400: "Bad Request"},
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(instance=post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="게시글 삭제",
        operation_description="게시글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request"},
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
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
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_id="게시글 수정",
        operation_description="게시글을 수정합니다.",
        request_body=PostDetailRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
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
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.title = title
        post.content = content

        tag_contents = request.data.get("tags")
        if tag_contents is not None:
            post.tags.clear()
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        post.save()
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LikeView(APIView):
    @swagger_auto_schema(
        operation_id="좋아요 토글",
        operation_description="좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.",
        request_body=SignInRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request, post_id):

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ### 2 ###
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        ### 3 ###
        is_liked = post.like_set.filter(user=author).count() > 0

        ### 4 ###
        if is_liked == True:
            post.like_set.get(user=author).delete()
            print("좋아요 취소")
        else:
            Like.objects.create(user=author, post=post)
            print("좋아요 누름")

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="특정 글에 달린 모든 댓글을 조회합니다.",
        manual_parameters=[
        openapi.Parameter(
            'post', openapi.IN_QUERY, description="게시글 ID", type=openapi.TYPE_INTEGER, required=True
        )
    ],
        responses={200: CommentSerializer(many=True), 404: "Not Found", 400: "Bad Request"},
    )
    def get (self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({"error": "post 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentRequestSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        }
    )
    def post(self, request):
        try:
            post_id = request.data.get("post")
            content = request.data.get("content")
            author_info = request.data.get("author")

            if not post_id or not content or not author_info:
                return Response(
                    {"detail": "필수 필드가 누락되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = author_info.get("username")
            password = author_info.get("password")

            if not username or not password:
                return Response(
                    {"detail": "username 또는 password가 누락되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                author = User.objects.get(username=username)
                if not author.check_password(password):
                    return Response(
                        {"detail": "비밀번호가 틀렸습니다."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except User.DoesNotExist:
                return Response(
                    {"detail": "유저를 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response(
                    {"detail": "게시글을 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )

            comment = Comment.objects.create(
                post=post,
                content=content,
                author=author
            )

            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": f"알 수 없는 오류: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CommentDetailView(APIView):

    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="자신이 작성한 댓글만 수정이 가능합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            403: "Unauthorized or No Permission",
            404: "Not Found"
        }
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "댓글을 찾을 수 없습니다."}, status=404)

        data = request.data
        author_info = data.get("author")
        content = data.get("content")

        if not author_info or not content:
            return Response({"detail": "필수 필드가 누락되었습니다."}, status=400)

        username = author_info.get("username")
        password = author_info.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "작성자를 찾을 수 없습니다."}, status=404)

        if not user.check_password(password):
            return Response({"detail": "비밀번호가 틀렸습니다."}, status=403)

        if comment.author != user:
            return Response({"detail": "수정 권한이 없습니다."}, status=403)

        comment.content = content
        comment.save()
        return Response(CommentSerializer(comment).data, status=200)

    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="자신이 작성한 댓글만 삭제할 수 있습니다.",
        request_body=SignInRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            403: "Unauthorized",
            404: "Not Found"
        }
    )
    def delete(self, request, comment_id):
        author_info = request.data
        if not author_info:
            return Response({"detail": "author 정보가 없습니다."}, status=400)

        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response({"detail": "username 또는 password가 없습니다."}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "작성자를 찾을 수 없습니다."}, status=404)

        if not user.check_password(password):
            return Response({"detail": "비밀번호가 틀렸습니다."}, status=403)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "댓글을 찾을 수 없습니다."}, status=404)

        if comment.author != user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=403)

        comment.delete()
        return Response(status=204)