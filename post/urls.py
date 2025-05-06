from django.urls import path
### 추가
from .views import PostListView, PostDetailView
###

app_name = 'post'

# api/post/로 시작하는 url은 이곳으로 왔다.
# 그 이후에 붙는 것부터 여기서 찾는 것이다.
# 예) api/post/3이라면 <int:post_id>로
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), ### 추가 // post/로 들어오면 PostListView를 보여줘라 -> 이것들은 위에서 .views에서 import 해온 것들.
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가 // post/3으로 들어오면 PostDetailView를 보여줘라

]