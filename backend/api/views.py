from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    ServiceWithTermsSerializer,
    UserGETSerializer,
    CategorySerializer,
    TermDetailSerializer,
    SubscriptionSerializer
)
from services.models import Category, Service, Subscription, Terms
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404


class MeView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = UserGETSerializer(request.user)
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

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
