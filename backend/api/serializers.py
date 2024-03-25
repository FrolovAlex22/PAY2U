from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.db.models import Min, Max

from users.models import User
from services.models import BankCard, Category, Service, Subscription, Terms


class UserSerializer(UserSerializer):
    """При просмотре страницы пользователя"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class ServiceSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    max_cashback = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ('name', 'image', 'subscription_type', 'text', 'category', 'min_price', 'max_cashback', 'is_featured')

    def get_min_price(self, obj):
        min_price = obj.subscription_terms.aggregate(min_price=Min('price'))['min_price']
        return min_price if min_price is not None else 0

    def get_max_cashback(self, obj):
        max_cashback = obj.subscription_terms.aggregate(max_cashback=Max('cashback'))['max_cashback']
        return max_cashback if max_cashback is not None else 0


class TermsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terms
        fields = ('id', 'name', 'price', 'duration', 'cashback')


class ServiceWithTermsSerializer(serializers.ModelSerializer):
    subscription_terms = TermsSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'image', 'text', 'subscription_terms')


class TermDetailSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_image = serializers.ImageField(source='service.image', read_only=True)
    service_category = serializers.CharField(source='service.category', read_only=True)
    class Meta:
        model = Terms
        fields = ('id', 'name', 'subscription_type', 'duration', 'cashback', 'price', 'service_name', 'service_image', 'service_category')


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ['id', 'card_number']


class SubscriptionSerializer(serializers.ModelSerializer): # при обновление подписки даты просуммировать
    bank_card_details = BankCardSerializer(source='bank_card', read_only=True)
    terms_details = TermDetailSerializer(source='terms', read_only=True)

    class Meta:
        model = Subscription
        fields = ['start_date', 'end_date', 'bank_card_details', 'terms_details']
        extra_kwargs = {'end_date': {'required': False}}

    def create(self, validated_data):
        user = validated_data.get('user')
        terms = validated_data.get('terms')

        bank_card = BankCard.objects.filter(user=user).first()
        if not bank_card:
            raise serializers.ValidationError("У пользователя нет банковской карты для привязки к подписке.")

        if bank_card.balance < terms.price:
            raise serializers.ValidationError("На банковской карте недостаточно средств для оформления подписки.")

        with transaction.atomic():
            bank_card.balance -= terms.price
            bank_card.save()

            duration_mapping = {
                "one_month": 30,
                "three_months": 90,
                "six_months": 180,
                "one_year": 365,
            }
            duration_days = duration_mapping.get(terms.duration, 30)
            validated_data['end_date'] = validated_data.get('start_date', timezone.now()) + timedelta(days=duration_days)

            subscription = Subscription.objects.create(**validated_data, bank_card=bank_card)

        return subscription
