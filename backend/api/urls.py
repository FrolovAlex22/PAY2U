from django.urls import include, path
from rest_framework import routers

from .views import TermsViewSet, CategoryViewSet, MeView

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('terms', TermsViewSet, basename='terms')
app_name = 'api'

urlpatterns = [
    path("me/", MeView.as_view(), name="user-me"),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path("auth/", include("djoser.urls.jwt")),
]
