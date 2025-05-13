from django.urls import path
### 추가
from .views import CommentListView, CommentDetailView
###

app_name = 'comment'

# api/comment/로 시작하는 url은 이곳으로 왔다.
# 그 이후에 붙는 것부터 여기서 찾는 것이다.
# 예) api/comment/3이라면 <int:comment_id>로
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가
    path("<int:comment_id>/", CommentDetailView.as_view()), ### 추가

]