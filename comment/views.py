from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status
from drf_yasg.utils          import swagger_auto_schema
from drf_yasg                import openapi

from post.models            import Post
from account.models         import User
from .models                import Comment
from .serializers           import CommentSerializer
from .request_serializers   import (
    CommentCreateRequestSerializer,
    CommentUpdateRequestSerializer,
    CommentDeleteRequestSerializer,
)


class CommentListCreateView(APIView):

    # ----------------------- 댓글 목록 조회 -----------------------
    @swagger_auto_schema(
        operation_id="댓글_목록_조회",
        operation_description="쿼리 파라미터 `?post=<postId>` 로 전달된 포스트의 모든 댓글을 조회합니다.",
        request_body=None,
        manual_parameters=[
            openapi.Parameter(
                name="post",
                in_=openapi.IN_QUERY,
                description="조회할 Post의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=123,
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK",
                schema=CommentSerializer(many=True)
            ),
            404: "Post not found",
        },
    )
    def get(self, request):
        post_id = request.GET.get("post")
        if not post_id:
            return Response(
                {"message": "missing query parameter 'post'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        qs = Comment.objects.filter(post=post)
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------------------- 댓글 생성 -----------------------
    @swagger_auto_schema(
        operation_id="댓글_생성",
        operation_description="새로운 댓글을 작성합니다.",
        request_body=CommentCreateRequestSerializer,
        responses={
            201: openapi.Response(
                description="Created",
                schema=CommentSerializer()
            ),
            400: "Bad Request",
            403: "Forbidden",  # 비밀번호 불일치
            404: "Author or Post not found",
        },
    )
    def post(self, request):
        # 1) 요청 데이터 검증
        req_ser = CommentCreateRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        data = req_ser.validated_data

        # 2) author 인증
        author_data = data["author"]
        try:
            user = User.objects.get(
                email=author_data["email"],
                username=author_data["username"],
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not user.check_password(author_data["password"]):
            return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3) post 존재 확인
        try:
            post = Post.objects.get(id=data["post"])
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 4) Comment 생성
        comment = Comment.objects.create(
            author=user,
            post=post,
            content=data["content"],
        )
        out_ser = CommentSerializer(comment)
        return Response(out_ser.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):

    # ----------------------- 댓글 수정 -----------------------
    @swagger_auto_schema(
        operation_id="댓글_수정",
        operation_description="작성자가 작성한 댓글을 수정합니다.",
        request_body=CommentUpdateRequestSerializer,
        responses={
            200: openapi.Response(description="OK", schema=CommentSerializer()),
            400: "Bad Request",
            401: "Unauthorized",  # 인증/권한 오류
            404: "Not Found",
        },
        manual_parameters=[
            openapi.Parameter(
                name="comment_id",
                in_=openapi.IN_PATH,
                description="수정할 Comment의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def put(self, request, comment_id):
        # 1. Request Data Validation
        req_ser = CommentUpdateRequestSerializer(data=request.data)
        if not req_ser.is_valid():
            return Response(req_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        data = req_ser.validated_data

        # 2. Retrieve Comment Object
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 3. Authenticate and Authorize User
        author_data = data["author"]
        try:
            user_to_authenticate = User.objects.get(
                email=author_data["email"],
                username=author_data["username"],
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if comment.author != user_to_authenticate:
            return Response(
                {"message": "Permission denied. You are not the author of this comment."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user_to_authenticate.check_password(author_data["password"]):
            return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 4. Update Comment
        comment.content = data["content"]
        comment.save()

        out_ser = CommentSerializer(comment)
        return Response(out_ser.data, status=status.HTTP_200_OK)

    # ----------------------- 댓글 삭제 -----------------------
    @swagger_auto_schema(
        operation_id="댓글_삭제",
        operation_description="작성자가 작성한 댓글만 삭제할 수 있습니다.",
        request_body=CommentDeleteRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",  # 인증/권한 오류
            404: "Not Found",
        },
        manual_parameters=[
            openapi.Parameter(
                name="comment_id",
                in_=openapi.IN_PATH,
                description="삭제할 Comment의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def delete(self, request, comment_id):
        req_ser = CommentDeleteRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        auth_data = req_ser.validated_data

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user = User.objects.get(
                email=auth_data["email"],
                username=auth_data["username"],
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if comment.author != user:
            return Response(
                {"message": "Permission denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.check_password(auth_data["password"]):
            return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
