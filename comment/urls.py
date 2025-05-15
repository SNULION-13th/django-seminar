from django.urls import path
from .views import CommentView, CommentDetailView

urlpatterns = [
    path('', CommentView.as_view()), # 특정 게시물 comment 다 불러오기 / comment create(id 자동 부여)
    path('<int:comment_id>/', CommentDetailView.as_view()), # 특정 comment 업데이트. 권한 있을때만 업뎃 가능 / 특정 comment 삭제. 마찬가지로 권한 있을때만 삭제 가능.
]
