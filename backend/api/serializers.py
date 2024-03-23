from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.db.models import Min, Max

from users.models import User
from services.models import BankCard, Category, Service, Subscription, Terms


class UserGETSerializer(UserSerializer):
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


class ServiceSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    max_cashback = serializers.SerializerMethodField()

    def get_min_price(self, obj):
        return obj.subscription_terms.aggregate(min_price=Min('price'))['min_price']

    def get_max_cashback(self, obj):
        return obj.subscription_terms.aggregate(max_cashback=Max('cashback'))['max_cashback']

    class Meta:
        model = Service
        fields = ('name', 'image', 'text', 'category', 'min_price', 'max_cashback')


class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'services')


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
    service_name = serializers.SerializerMethodField()

    def get_service_name(self, obj):
        return obj.service.name

    class Meta:
        model = Terms
        fields = ('id', 'name', 'duration', 'cashback', 'price', 'service_name')


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ['id', 'card_number']


class SubscriptionSerializer(serializers.ModelSerializer):
    bank_card_details = BankCardSerializer(source='bank_card', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    terms_details = TermsSerializer(source='terms', read_only=True)

    class Meta:
        model = Subscription
        fields = ['service', 'terms', 'start_date', 'end_date', 'bank_card_details', 'service_details', 'terms_details']
        extra_kwargs = {'end_date': {'required': False}}

    def create(self, validated_data):
        user = validated_data.get('user')
        terms = validated_data.get('terms')

        bank_card = BankCard.objects.filter(user=user).first()
        if not bank_card:
            raise serializers.ValidationError("User does not have a bank card to associate with the subscription.")

        if bank_card.balance < terms.price:
            raise serializers.ValidationError("Not enough funds on the bank card to subscribe.")

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
