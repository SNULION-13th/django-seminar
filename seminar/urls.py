from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', include('post.urls')), #post 폴더의 urls.py 파일로 가서 이후 url을 찾아라
]