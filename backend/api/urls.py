from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, CustomUserViewSet, ServiceViewSet, SubscriptionViewSet, MainPageAPIView, ComparisonAPIView


router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'user', CustomUserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    # path('expenses/', ExpensesView.as_view(), name='user-expenses'),
    path('main/', MainPageAPIView.as_view(), name='main'),
    path('comparison/', ComparisonAPIView.as_view(), name='main'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]