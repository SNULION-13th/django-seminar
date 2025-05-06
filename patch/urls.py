from django.urls import path
from .views import PostUpdateView

app_name = 'patch'

urlpatterns = [
    # CBV url path
    path("", PostUpdateView.as_view()),
    path("posts/<int:id>/", PostUpdateView.as_view()),

]