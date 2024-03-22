from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from api.serializers import (
    UserGETSerializer,
    CategorySerializer,
    TermsSerializer,
)
from services.models import Category, Terms
from rest_framework.response import Response


class MeView(APIView):
    """Представление для получения данных о текущем пользователе."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Получение данных о текущем пользователе."""
        serializer = UserGETSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class TermsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса SubscriptionTerms"""

    queryset = Terms.objects.all()
    serializer_class = TermsSerializer
    permission_classes = (AllowAny,)
