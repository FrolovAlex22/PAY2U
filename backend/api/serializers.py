import base64
from django.core.files.base import ContentFile
from django.db import transaction
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User
from services.models import (
    Category, Terms, Service, TermsInService, Subscription
)
from PAY2U.settings import SERVICES_LIMIT


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для кодирования изображения в base64."""

    def to_internal_value(self, data):
        """Метод преобразования картинки"""

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)

class CustomUserSerializer(UserSerializer):
    """При просмотре страницы пользователя"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone_number'
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """При создании пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'phone_number',
            'password',
        )


class CategorySerializer(ModelSerializer):
    """Сериализатор для вывода категории"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Category
        fields = ('id', 'name', 'text')


class TermsSerializer(ModelSerializer):
    """Сериализатор для вывода категории"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Terms
        fields = ('id', 'name', 'duration', 'price', 'cashback')


class TermsInServiseSerializer(ModelSerializer):
    """Сериализатор для модели условий в рецепте"""

    id = serializers.ReadOnlyField(source='terms.id')
    name = serializers.ReadOnlyField(source='terms.name')
    duration = serializers.ReadOnlyField(source='terms.duration')
    price = serializers.ReadOnlyField(source='terms.price')
    cashback = serializers.ReadOnlyField(source='terms.cashback')

    class Meta:
        """Мета-параметры сериализатора"""

        model = TermsInService
        fields = ('id', 'name', 'duration', 'price', 'cashback')


class ServiceSerializer(ModelSerializer):
    category = CategorySerializer()
    service_terms = TermsInServiseSerializer(
        source='services_list'
    )

    class Meta:
        """Мета-параметры сериализатора"""

        model = Service
        fields = (
            'id', 'name', 'category','image', 'text',
            'service_terms'
        )


class CreateTermsInServiseSerializer(ModelSerializer):
    """Сериализатор для модели условий в рецепте"""

    id = serializers.IntegerField()

    class Meta:
        """Мета-параметры сериализатора"""

        model = TermsInService
        fields = ('id')

class CreateServiceSerializer(ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    service_terms = CreateTermsInServiseSerializer()
    image = Base64ImageField(use_url=True)

    class Meta:
        """Мета-параметры сериализатора"""

        model = Service
        fields = (
            'id', 'name', 'category','image', 'text',
            'service_terms'
        )


    def to_representation(self, instance):
        """Метод представления модели"""

        serializer = ServiceSerializer(
            instance,
            context={'request': self.context['request']}
        )
        return serializer.data

    def validate_category(self, data):
            """Метод валидации категории"""

            category = self.initial_data.get('category')

            if not category:
                raise serializers.ValidationError(
                    'Для создания сервиса выберите категорию!'
                )

            return data


    def validate_service_terms(self, data):
            """Метод валидации условий"""

            terms = self.initial_data.get('service_terms')

            if not terms:
                raise serializers.ValidationError(
                    'Для создания сервиса укажите условия!'
                )

            return data


    def create_terms(self, service_terms, service):
        """Метод создания условия"""

        id = service_terms['id']
        terms = Terms.objects.get(pk=id)
        TermsInService.objects.create(terms=terms, service=service)

    def create_category(self, category, service):
        """Метод добавления категории"""

        service.category.set(category)

    def create(self, validated_data):
        """Метод создания модели"""

        category = validated_data.pop('category')
        service_terms = validated_data.pop('service_terms')
        service = Service.objects.create(**validated_data)
        self.create_terms(service_terms, service)
        self.create_category(category, service)
        return service

    @transaction.atomic
    def update(self, instance, validated_data):
        """Метод обновления модели"""

        TermsInService.objects.filter(service=instance).delete()
        self.validate_category(validated_data)
        self.validate_service_terms(validated_data)
        self.create_terms(validated_data.pop('service_terms'), instance)
        self.create_category(validated_data.pop('category'), instance)

        return super().update(instance, validated_data)


class CatalogSerializer(CategorySerializer):
    """Подписка"""

    services = serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = (
            'name',
            'text',
            'services',
        )

    def get_services(self, obj):
        """Получение списка рецептов автора"""

        categorys_services = obj.services.all()[:SERVICES_LIMIT]

        if categorys_services:
            serializer = AdditionalForServiceSerializer(
                categorys_services,
                context={'request': self.context['request']},
                many=True,
            )
            return serializer.data

        return []


class ServiceTermsForCatalogSerializer(ModelSerializer):
    """Сериализатор для компактного отображения условий сервиса"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Terms
        fields = ('name', 'duration', 'cashback')


class AdditionalForServiceSerializer(ModelSerializer):
    """Сериализатор для компактного отображения сервисов"""
    service_terms = ServiceTermsForCatalogSerializer()

    class Meta:
        """Мета-параметры сериализатора"""

        model = Service
        fields = ('id', 'name', 'image', 'service_terms')

class SubscriptionSerializer(ModelSerializer):
    """Подписка"""

    id = serializers.ReadOnlyField(source='user_subscriptions.id')
    name = serializers.ReadOnlyField(source='user_subscriptions.name')
    category = serializers.ReadOnlyField(source='user_subscriptions.category')
    image = serializers.ReadOnlyField(source='user_subscriptions.image')
    service_terms = ServiceTermsForCatalogSerializer(
        source='user_subscriptions.service_terms'
    )

    class Meta:
        model = Subscription
        fields = (
            'id',
            'name',
            'category',
            'image',
            'text',
            'service_terms',
        )
