from django.urls import path
from .views import CommentView, CommentDetailView

urlpatterns = [
    path("comment/", CommentView.as_view()),
    path("comment/<int:comment_id>/", CommentDetailView.as_view()),
]
