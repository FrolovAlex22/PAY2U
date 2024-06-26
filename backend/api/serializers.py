from django.db.models import Sum
from djoser.serializers import UserSerializer
from rest_framework import serializers

from services.models import (
    BankCard,
    Category,
    Comparison,
    Service,
    Subscription,
    Terms
)
from PAY2U.settings import SUBSCRIBE_LIMIT
from users.models import User


class UserSerializer(UserSerializer):
    """При просмотре страницы пользователя"""

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number'
        ]


class CustomUserCreateSerializer(UserSerializer):
    """Сериализатор при создании пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'phone_number',
            'password',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    services = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'services']

    def get_services(self, obj):
        """Получение списка сервисов категории"""

        categorys_services = obj.services.all()[:SUBSCRIBE_LIMIT]

        if categorys_services:
            serializer = AdditionalForServiceSerializer(
                categorys_services,
                context={'request': self.context['request']},
                many=True,
            )
            return serializer.data

        return []


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор сервисов"""
    min_price = serializers.SerializerMethodField()
    max_cashback = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'name', 'image', 'text', 'category', 'min_price', 'max_cashback',
            'is_featured'
        ]

    def get_min_price(self, obj):
        min_price = obj.min_price
        return min_price if min_price is not None else 0

    def get_max_cashback(self, obj):
        max_cashback = obj.max_cashback
        return max_cashback if max_cashback is not None else 0


class TermsSerializer(serializers.ModelSerializer):
    """Сериализатор условий подписок"""
    class Meta:
        model = Terms
        fields = ['id', 'name', 'price', 'duration', 'cashback']


class ServiceWithTermsSerializer(serializers.ModelSerializer):
    """Сериализатор сервиса с условиями """
    subscription_terms = TermsSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'image', 'text', 'subscription_terms']


class TermDetailSerializer(serializers.ModelSerializer):
    """Сериализатор деталей условия подписки"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_image = serializers.ImageField(
        source='service.image',
        read_only=True
    )
    service_category = serializers.CharField(
        source='service.category',
        read_only=True
    )

    class Meta:
        model = Terms
        fields = [
            'id', 'name', 'subscription_type', 'duration', 'cashback', 'price',
            'service_name', 'service_image', 'service_category'
        ]


class BankCardSerializer(serializers.ModelSerializer):
    """Сериализатор банковской карты"""
    class Meta:
        model = BankCard
        fields = ['id', 'card_number', 'is_active', 'balance']


class ExpenseSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения расходов"""
    service_name = serializers.CharField(source='service.name')
    category_name = serializers.CharField(source='service.category.name')
    price = serializers.DecimalField(
        source='terms.price',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = Subscription
        fields = ['service_name', 'category_name', 'price', 'start_date']


class PaidSerializer(serializers.ModelSerializer):
    """Сериализатор для получения оплаты"""
    service_name = serializers.CharField(source='service.name')
    category_name = serializers.CharField(source='service.category.name')
    price = serializers.DecimalField(
        source='terms.price',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = Subscription
        fields = ['service_name', 'category_name', 'price', 'end_date']


class CashbackSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения кэшбэка пользователя"""
    cashback_amount = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name')
    category_name = serializers.CharField(source='service.category.name')

    class Meta:
        model = Subscription
        fields = ['service_name', 'category_name', 'cashback_amount']

    def get_cashback_amount(self, obj):
        """Получений суммы кэшбэка для конретного сервиса"""
        return obj.terms.price * (obj.terms.cashback / 100)


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор личной страницы пользователя"""
    service = serializers.ReadOnlyField(source='service.name')
    category = serializers.ReadOnlyField(source='service.category.name')
    image = serializers.ImageField(source='service.image')
    price = serializers.IntegerField(source='terms.price')
    cashback = serializers.IntegerField(source='terms.cashback')
    bank_card = serializers.IntegerField(source='bank_card.card_number')

    class Meta:
        model = Subscription
        fields = [
            'id', 'service', 'category', 'image', 'price',
            'cashback', 'end_date', 'bank_card'
        ]


class TermsPriceCashbackSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения цены и кэшбэка для сервиса"""

    class Meta:
        model = Terms
        fields = ['price', 'cashback']


class BestOfferSerializer(serializers.ModelSerializer):
    cashback = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'image', 'cashback']

    def get_cashback(self, obj):
        """Получить сумму кэшбэка"""
        terms = Terms.objects.filter(service=obj.id, is_featured=True)
        serializer = TermsPriceCashbackSerializer(terms, many=True)
        return serializer.data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок пользователя"""
    bank_card_details = BankCardSerializer(source='bank_card', read_only=True)
    terms_details = TermDetailSerializer(source='terms', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'start_date', 'end_date', 'bank_card_details', 'terms_details'
        ]


class MainSubscriptionSerializer(serializers.ModelSerializer):
    """Дополнительный сериализатор главной страницы для обработки подписок
    пользователя"""
    service_name = serializers.CharField(source='service.name')
    service_image = serializers.ImageField(source='service.image')
    terms_price = serializers.IntegerField(source='terms.price')

    class Meta:
        model = Subscription
        fields = ('service_name', 'service_image', 'terms_price')


class MainPageSerializer(serializers.ModelSerializer):
    """Сериализатор главной страницы"""
    best_offer = serializers.SerializerMethodField()
    subscription = MainSubscriptionSerializer(
        many=True,
        source='subscriptions',
        read_only=True
    )
    total_cashback = serializers.SerializerMethodField()
    total_expenses = serializers.SerializerMethodField()
    total_paids = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'best_offer', 'subscription', 'total_cashback',
            'total_expenses', 'total_paids'
        ]

    def get_best_offer(self, obj):
        """Лучшее предложение"""
        featured_services = Service.objects.filter(is_featured=True)
        serializer = ServiceSerializer(
            featured_services,
            many=True,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def get_total_cashback(self, obj):
        """Общий кэшбэк"""
        queryset = obj.subscriptions.all()
        return sum(
            sub.terms.price * (sub.terms.cashback / 100) for sub in queryset
        )

    def get_total_expenses(self, obj):
        """Общая сумма рассходов"""
        queryset = obj.subscriptions.all()
        return (
            queryset.aggregate(Sum('terms__price'))['terms__price__sum'] or 0
        )

    def get_total_paids(self, obj):
        """Общая сумма к оплате"""
        queryset = obj.subscriptions.all()
        return (
            queryset.aggregate(Sum('terms__price'))['terms__price__sum'] or 0
        )


class ServiceTermsForCatalogSerializer(serializers.ModelSerializer):
    """Сериализатор для компактного отображения условий сервиса"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Terms
        fields = ('cashback', 'price')


class ComparisonSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения сравнений"""
    name = serializers.ReadOnlyField(source='service.name')
    image = serializers.ImageField(source='service.image')
    min_price = serializers.SerializerMethodField()
    max_cashback = serializers.SerializerMethodField()

    class Meta:
        """Мета-параметры сериализатора"""

        model = Comparison
        fields = ('id', 'name', 'image', 'min_price', 'max_cashback')

    def get_min_price(self, obj):
        """Минимальная цена подписки"""
        service = Service.objects.get(id=obj.service.id)
        min_price = service.min_price
        return min_price if min_price is not None else 0

    def get_max_cashback(self, obj):
        """Максимальный кэшбек сервиса"""
        service = Service.objects.get(id=obj.service.id)
        max_cashback = service.max_cashback
        return max_cashback if max_cashback is not None else 0


class AdditionalForServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для компактного отображения сервисов"""
    service_terms = serializers.SerializerMethodField()

    class Meta:
        """Мета-параметры сериализатора"""

        model = Service
        fields = ('id', 'name', 'image', 'service_terms')

    def get_service_terms(self, obj):
        """Получение списка условий сервиса"""

        categorys_services = Terms.objects.filter(service=obj.id)

        serializer = ServiceTermsForCatalogSerializer(
                categorys_services,
                context={'request': self.context['request']},
                many=True,
            )
        return serializer.data


class CatalogSerializer(serializers.ModelSerializer):
    """Подписка"""
    services = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'services',
        )

    def get_services(self, obj):
        """Получение списка рецептов автора"""

        categorys_services = obj.services.all()[:SUBSCRIBE_LIMIT]

        if categorys_services:
            serializer = AdditionalForServiceSerializer(
                categorys_services,
                context={'request': self.context['request']},
                many=True,
            )
            return serializer.data

        return []
