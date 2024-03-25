from .filters import ServiceFilter, SubscriptionFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    ServiceWithTermsSerializer,
    UserSerializer,
    ServiceSerializer,
    TermDetailSerializer,
    SubscriptionSerializer,
    CategorySerializer
)
from services.models import Category, Service, Subscription, Terms
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action

class MeView(APIView): # представление взять у Саши, к нему добавить action методы для расчета кэшбека, оплаты и расходов

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_class = ServiceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceSerializer
        elif self.action == 'retrieve':
            return ServiceWithTermsSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=('get',), url_path='terms/(?P<term_pk>[^/.]+)')
    def term_detail(self, request, pk=None, term_pk=None):
        service = self.get_object()
        term = get_object_or_404(Terms, pk=term_pk, service=service)
        serializer = TermDetailSerializer(term)
        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscriptionFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
