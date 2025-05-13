from django.urls import path
from .views import CommentList,CommentCreate, CommentUpdate


app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentCreate.as_view()),
    path("<int:post_id>", CommentList.as_view()),
    path("<int:commentId>/",CommentUpdate.as_view()),
]