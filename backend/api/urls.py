from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, ExpensesView, CustomUserViewSet, ServiceDetailView, TermDetailAPIView, SubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'user', CustomUserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('expenses/', ExpensesView.as_view(), name='user-expenses'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:service_pk>/<int:term_pk>/', TermDetailAPIView.as_view(), name='service-term-detail'),
    # path("me/", MeView.as_view(), name="user-me"),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path("auth/", include("djoser.urls.jwt")),
]
