import datetime
from django.db.models import Q, Sum

from .filters import ServiceFilter, SubscriptionFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import (
    BankCardSerializer,
    ComparisonSerializer,
    ExpenseSerializer,
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
        serializer = UserSubscribeSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def cashback(self, request):
        """Кэшбэк пользователя"""
        user = self.request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        category = request.query_params.get('category')
        filters = Q(user=user)
        if category:
            filters &= Q(service__category__name=category)

        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            filters &= Q(start_date__date__gte=start_date)
        
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            filters &= Q(start_date__date__lte=end_date)

        queryset = Subscription.objects.filter(filters)
        
        if not queryset.exists():
            return Response({'errors': 'По заданным параметрам подписок не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        total_cashback = sum(sub.terms.price * (sub.terms.cashback / 100) for sub in queryset)

        serializer = CashbackSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        data.append({'total_cashback': total_cashback})
        return Response(data)


    @action(
        detail=False,
        methods=('get',),
    )
    def expenses(self, request):
        """Расходы пользователя с возможностью фильтрации по датам"""
        user = self.request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        category = request.query_params.get('category')
        filters = Q(user=user)
        if category:
            filters &= Q(service__category__name=category)

        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            filters &= Q(start_date__date__gte=start_date)
        
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            filters &= Q(start_date__date__lte=end_date)

        queryset = Subscription.objects.filter(filters)
        
        if not queryset.exists():
            return Response({'errors': 'По заданным параметрам подписок не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        
        total_expenses = queryset.aggregate(Sum('terms__price'))['terms__price__sum'] or 0
        serializer = ExpenseSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        data.append({'total_expenses': total_expenses})
        return Response(data)


    @action(
        detail=False,
        methods=('get',),
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


class BankCardView(APIView):

    def get(self, request):
        cards = BankCard.objects.filter(user=request.user)
        serializer = BankCardSerializer(cards, many=True)
        return Response(serializer.data)

    def patch(self, request):
        card_id = request.data.get('card_id')
        if not card_id:
            return Response({'error': 'Необходимо указать card_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            card_to_activate = BankCard.objects.get(id=card_id, user=request.user)
        except BankCard.DoesNotExist:
            return Response({'error': 'Карта не найдена'}, status=status.HTTP_404_NOT_FOUND)

        if card_to_activate.is_active:
            return Response({'message': 'Эта карта уже активирована'}, status=status.HTTP_200_OK)

        BankCard.objects.filter(user=request.user, is_active=True).update(is_active=False)
        card_to_activate.is_active = True
        card_to_activate.save()

        return Response({'message': 'Карта активирована'}, status=status.HTTP_200_OK)
