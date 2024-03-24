from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, CategoryViewSet, TermsViewSet

router = routers.DefaultRouter()
router.register('catalog', CustomUserViewSet, basename='services')
router.register('profile', CustomUserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('terms', TermsViewSet, basename='terms')
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]