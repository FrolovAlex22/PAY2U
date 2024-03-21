from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import User

class CustomUserSerializer(UserSerializer):
    """Проверка подписки"""

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