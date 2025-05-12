from django.urls import path
from .views import CommentList

app_name = 'comment'
urlpatterns = [
    path('', CommentList.as_view()),
]
