from datetime import timedelta, timezone
from .filters import ServiceFilter, SubscriptionFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    CatalogSerializer,
    ComparisonSerializer,
    MainPageSerializer,
    ServiceWithTermsSerializer,
    UserSerializer,
    ServiceSerializer,
    TermDetailSerializer,
    SubscriptionSerializer,
    CashbackSerializer,
    CategorySerializer,
    UserSubscribeSerializer
)
from services.models import BankCard, Category, Comparison, Service, Subscription, Terms
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from djoser.views import UserViewSet
from users.models import User
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter


class MainPageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = MainPageSerializer(
            request.user
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComparisonAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        comparsion_list = user.user_comparison.all()
        serializer = ComparisonSerializer(
            comparsion_list, many=True, context={'request': request},
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Список подписок пользователя"""
        user = self.request.user
        queryset = user.subscriptions.all()
        pages = self.paginate_queryset(queryset)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

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
            url_path='profile',
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


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def catalog(self, request):
        """Каталог пользователя разбитый на категории"""
        queryset = Category.objects.all()
        pages = self.paginate_queryset(queryset)
        serializer = CatalogSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)



class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    filterset_class = ServiceFilter
    ordering_fields = ['name', '-name', 'min_price', '-min_price', 'max_cashback', '-max_cashback'] # разобраться с популярностью


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

    @action(
        detail=True,
        methods=('post', 'delete'),)
    def subscribe(self, request, pk=None):
        """Подписка на сервис"""
        user = self.request.user
        service = get_object_or_404(Service, id=pk)
        queryset = user.subscriptions.all()
        bank_card = BankCard.objects.filter(user=user).first()
        terms = Terms.objects.filter(service=service).first()

        if not bank_card:
            return Response(
                {'errors': 'У пользователя нет банковской карты для привязки к подписке.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.request.method == 'POST':
            duration_mapping = {
                "one_month": 30,
                "three_months": 90,
                "six_months": 180,
                "one_year": 360,
            }
            duration_days = duration_mapping.get(terms.duration, 30)
            summ_to_pay = (terms.price * (duration_days / 30))
            if bank_card.balance < summ_to_pay:
                return Response(
                    {'errors': 'На банковской карте недостаточно средств для оформления подписки.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            start_date = timezone.now()
            end_date = start_date + timedelta(days=duration_days)
            if Subscription.objects.filter(service=service, user=user, terms = terms):
                return Response(
                    {'errors': 'Вы уже подписаны на этот сервер.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = Subscription.objects.create(service=service, user=user, terms = terms, start_date=start_date, end_date=end_date, bank_card=bank_card)
            bank_card.balance -= summ_to_pay
            bank_card.save()
            serializer = SubscriptionSerializer(
                queryset, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not user.subscriptions.filter(service=pk):
                return Response(
                    {'errors': 'Вы не подписаны на этоn сервис!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscription = get_object_or_404(
                Subscription, user=user, service=service
            )
            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    @action(
        detail=True,
        methods=('post', 'delete'),)
    def add_comparison(self, request, pk=None):
        user = self.request.user
        service = get_object_or_404(Service, id=pk)
        if self.request.method == 'POST':
            if Comparison.objects.filter(service=service.id, user = user.id):
                return Response(
                    {'errors': 'Сервис уже в сравнении!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Comparison.objects.create(user=user, service=service)

            return Response(status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Comparison.objects.filter(service=service.id, user = user.id):
                return Response(
                    {'errors': 'Этого сервиса нет в сравнении!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscription = get_object_or_404(
                Comparison, service=service.id, user = user.id
            )
            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscriptionFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    