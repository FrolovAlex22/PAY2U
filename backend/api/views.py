from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response

from api.serializers import (
    CustomUserSerializer,
    CategorySerializer,
    TermsSerializer,
    ServiceSerializer,
    CreateServiceSerializer,
    CatalogSerializer,
    SubscriptionSerializer
)
from services.models import Category, Terms, Service, Subscription
from users.models import User



class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination 

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Список подписок пользователя"""
        user = self.request.user
        queryset = user.subscriber.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),)
    def subscribe(self, request, id=None):
        """Подписка на автора"""
        user = self.request.user
        service = get_object_or_404(Service, pk=id)

        if self.request.method == 'POST':
            if user.subscriber.filter(service=id):
                return Response(
                    {'errors': 'Подписка уже оформлена!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = Subscription.objects.create(service=service, user=user)
            serializer = SubscriptionSerializer(
                queryset, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not user.subscriber.filter(service=id):
                return Response(
                    {'errors': 'Вы не подписаны на этого пользователя!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscription = get_object_or_404(
                Subscription, user=user, service=service
            )
            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False,
            methods=['GET', 'PATCH'],
            url_path='me',
            url_name='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(
                request.user,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = CustomUserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def catalog(self, request):
        """Каталог пользователя разбитый на категории"""
        category = self.request.category
        queryset = category.category_services.all()
        pages = self.paginate_queryset(queryset)
        serializer = CatalogSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TermsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Terms"""

    queryset = Terms.objects.all()
    serializer_class = TermsSerializer
    permission_classes = (AllowAny,)


class ServiceViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с обьектами класса Recipe"""

    queryset = Service.objects.all()
    # pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return ServiceSerializer
        return CreateServiceSerializer

    def get_serializer_context(self):
        """Метод для передачи контекста """

        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


    # @action(
    #     detail=True,
    #     methods=('post', 'delete'),
    #     permission_classes=(IsAuthenticated,),
    #     url_path='favorite',
    #     url_name='favorite',
    # )
    # def favorite(self, request, pk):
    #     """Метод для управления избранными подписками """

    #     user = request.user
    #     if request.method == 'POST':
    #         if not Recipe.objects.filter(id=pk).exists():
    #             return Response(
    #                 {'errors': 'Вы пытаетесь добавить не существующий рецепт'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         recipe = get_object_or_404(Recipe, id=pk)
    #         if user.favorites.filter(recipe=pk):
    #             return Response(
    #                 {'errors': f'Рецепт - \"{recipe.name}\" нельзя добавить,'
    #                            f'он уже есть в избранном у пользователя.'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         Favorite.objects.create(user=user, recipe=recipe)
    #         serializer = AddFavoritesSerializer(recipe)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if request.method == 'DELETE':
    #         recipe = get_object_or_404(Recipe, id=pk)
    #         obj = user.favorites.filter(recipe=pk)
    #         if obj.exists():
    #             obj.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response(
    #             {'errors': f'В избранном нет рецепта \"{recipe.name}\"'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(
    #     detail=True,
    #     methods=('post', 'delete'),
    #     permission_classes=(IsAuthenticated,),
    #     url_path='shopping_cart',
    #     url_name='shopping_cart',
    # )
    # def shopping_cart(self, request, pk):
    #     """Метод для управления списком покупок"""

    #     user = request.user

    #     if request.method == 'POST':
    #         if not Recipe.objects.filter(id=pk).exists():
    #             return Response(
    #                 {'errors':
    #                  'Вы пытаетесь добавить не существующий рецепт!'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         recipe = get_object_or_404(Recipe, id=pk)
    #         if user.shopping_user.filter(recipe=pk):
    #             return Response(
    #                 {'errors': f'Повторно - \"{recipe.name}\" добавить нельзя,'
    #                            f'он уже есть в списке покупок'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         ShoppingCart.objects.create(user=user, recipe=recipe)
    #         serializer = AddFavoritesSerializer(recipe)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if request.method == 'DELETE':
    #         recipe = get_object_or_404(Recipe, id=pk)
    #         obj = user.shopping_user.filter(recipe=pk)
    #         if obj.exists():
    #             obj.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response(
    #             {'errors': f'Нельзя удалить рецепт - \"{recipe.name}\", '
    #                        f'его нет в списке покупок. '},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    # @staticmethod
    # def ingredients_to_txt(ingredients):
    #     """Метод для состовления списка ингредиентов для загрузки"""

    #     shopping_list = ''
    #     for ingredient in ingredients:
    #         shopping_list += (
    #             f'{ingredient["ingredient__name"]}  - '
    #             f'{ingredient["sum"]}'
    #             f'({ingredient["ingredient__measurement_unit"]})\n'
    #         )
    #     return shopping_list

    # @action(
    #     detail=False,
    #     methods=('get',),
    #     permission_classes=(IsAuthenticated,),
    #     url_path='download_shopping_cart',
    #     url_name='download_shopping_cart',
    # )
    # def download_shopping_cart(self, request):
    #     """Метод для загрузки ингредиентов и их количества
    #      для выбранных рецептов"""

    #     ingredients = IngredientInRecipe.objects.filter(
    #         recipe__shopping_recipe__user=request.user
    #     ).values(
    #         'ingredient__name',
    #         'ingredient__measurement_unit'
    #     ).annotate(sum=Sum('amount'))
    #     shopping_list = self.ingredients_to_txt(ingredients)
    #     return HttpResponse(shopping_list, content_type='text/plain')
