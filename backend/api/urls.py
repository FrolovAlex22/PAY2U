from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, CustomUserViewSet, ServiceViewSet, SubscriptionViewSet


router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'user', CustomUserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    # path('expenses/', ExpensesView.as_view(), name='user-expenses'),
    # path("me/", MeView.as_view(), name="user-me"),
    path('', include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
]
