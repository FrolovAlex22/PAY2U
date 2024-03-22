import base64
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User
from services.models import Category, Terms

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


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для кодирования изображения в base64."""

    def to_internal_value(self, data):
        """Метод преобразования картинки"""

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    """При создании пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'name',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        )


class CategorySerializer(ModelSerializer):
    """Сериализатор для вывода категории"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Category
        fields = ('id', 'name', 'text')


class  TermsSerializer(ModelSerializer):
    """Сериализатор для вывода категории"""

    class Meta:
        """Мета-параметры сериализатора"""

        model = Terms
        fields = ('id', 'name', 'duration', 'price', 'cashback')
