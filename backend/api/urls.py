from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('terms', CustomUserViewSet, basename='terms')
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]