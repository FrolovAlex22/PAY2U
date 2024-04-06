from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import (
    BankCardView,
    CategoryViewSet,
    CustomUserViewSet,
    ComparisonAPIView,
    MainPageAPIView,
    ServiceViewSet,
    SubscriptionViewSet,
)


router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(
    r'subscriptions', SubscriptionViewSet, basename='subscriptions'
)
router.register(r'user', CustomUserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('main/', MainPageAPIView.as_view(), name='main'),
    path('comparison/', ComparisonAPIView.as_view(), name='main'),
    path('cards/', BankCardView.as_view(), name='cards-list-and-activate'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += [
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]
