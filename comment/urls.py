from django.urls import path
from .views import CommentList, CommentDetailView

app_name = 'comment'
urlpatterns = [
    path('', CommentList.as_view()),
    path("<int:comment_id>/", CommentDetailView.as_view()),
]
