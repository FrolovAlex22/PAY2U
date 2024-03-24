from .filters import SubscriptionFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    ExpenseSerializer,
    ServiceWithTermsSerializer,
    UserSerializer,
    CategorySerializer,
    TermDetailSerializer,
    SubscriptionSerializer
)
from services.models import Category, Service, Subscription, Terms
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class MeView(APIView):

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


class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceWithTermsSerializer

class TermDetailAPIView(APIView):

    def get(self, request, service_pk, term_pk):
        term = get_object_or_404(Terms, pk=term_pk, service__pk=service_pk)
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



class ExpensesView(ListAPIView):
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscriptionFilter

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
