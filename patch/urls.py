from django.urls import path
from .views import PostUpdateView

app_name = 'patch'

urlpatterns = [
    path("", PostUpdateView.as_view()),
    path("posts/<int:post_id>/", PostUpdateView.as_view()),

]