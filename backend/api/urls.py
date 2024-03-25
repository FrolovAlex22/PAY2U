from django.urls import include, path
from rest_framework import routers

from .views import ServiceViewSet, MeView, SubscriptionViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

app_name = 'api'

urlpatterns = [
    path("me/", MeView.as_view(), name="user-me"),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path("auth/", include("djoser.urls.jwt")),
]
