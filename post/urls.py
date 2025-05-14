from django.urls import path
### 추가
from .views import PostListView, PostDetailView, LikeView, CommentListView, CommentDetailView
###

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가
    path("<int:post_id>/like/", LikeView.as_view()),
    path("comment/", CommentListView.as_view()),
    path("comment/<int:comment_id>/", CommentDetailView.as_view())
]