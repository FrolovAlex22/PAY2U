from .filters import SubscriptionFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    ExpenseSerializer,
    ServiceWithTermsSerializer,
    UserSerializer,
    CategorySerializer,
    TermDetailSerializer,
    SubscriptionSerializer,
    CashbackSerializer
)
from services.models import Category, Service, Subscription, Terms
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from users.models import User
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def cashback(self, request):
        """Кэшбэк пользователя"""
        user = self.request.user
        queryset = user.subscriptions.all()
        if not queryset:
            return Response(
                {'errors': 'Чтобы увидеть кэшбэк, нужно'
                 'подписаться хотябы на 1 сервис!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pages = self.paginate_queryset(queryset)
        serializer = CashbackSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def expenses(self, request):
        """Расходы пользователя"""
        user = self.request.user
        queryset = user.subscriptions.all()
        if not queryset:
            return Response(
                {'errors': 'Чтобы увидеть расходы, нужно'
                 'подписаться хотябы на 1 сервис!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pages = self.paginate_queryset(queryset)
        serializer = CashbackSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def paids(self, request):
        """К оплате в этом месяце пользователя"""
        user = self.request.user
        queryset = user.subscriptions.all()
        if not queryset:
            return Response(
                {'errors': 'Чтобы увидеть сколько нужно оплатить, нужно'
                 'подписаться хотябы на 1 сервис!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pages = self.paginate_queryset(queryset)
        serializer = CashbackSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            methods=['GET', 'PATCH'],
            url_path='me',
            url_name='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(
                request.user,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
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
