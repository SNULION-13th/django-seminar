from django.urls import path
### 추가
from .views import CommentListView, CommentDetailView, CommentUpdateDeleteView
###

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가,
    path("post=<int:post_id>/", CommentDetailView.as_view()),
    path("<int:comment_id>/", CommentUpdateDeleteView.as_view()),
]