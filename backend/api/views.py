from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CustomUserSerializer
from users.models import User



class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = CustomPagination

    # @action(
    #     detail=False,
    #     methods=('get',),
    #     permission_classes=(IsAuthenticated,),
    # )
    # def subscriptions(self, request):
    #     """Список подписок пользователя"""
    #     user = self.request.user
    #     queryset = user.follower.all()
    #     pages = self.paginate_queryset(queryset)
    #     serializer = SubscriptionSerializer(
    #         pages, many=True, context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)

    # @action(
    #     detail=True,
    #     methods=('post', 'delete'),
    # )
    # def subscribe(self, request, id=None):
    #     """Подписка на автора"""
    #     user = self.request.user
    #     author = get_object_or_404(User, pk=id)

    #     if self.request.method == 'POST':
    #         if user.follower.filter(author=id):
    #             return Response(
    #                 {'errors': 'Подписка уже оформлена!'},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         queryset = Subscription.objects.create(author=author, user=user)
    #         serializer = SubscriptionSerializer(
    #             queryset, context={'request': request}
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if self.request.method == 'DELETE':
    #         if not user.follower.filter(author=id):
    #             return Response(
    #                 {'errors': 'Вы не подписаны на этого пользователя!'},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         subscription = get_object_or_404(
    #             Subscription, user=user, author=author
    #         )
    #         subscription.delete()

    #         return Response(status=status.HTTP_204_NO_CONTENT)

    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @action(detail=False,
    #         methods=['GET', 'PATCH'],
    #         url_path='me',
    #         url_name='me',
    #         permission_classes=(IsAuthenticated,))
    # def me(self, request):
    #     if request.method == 'GET':
    #         serializer = CustomUserSerializer(
    #             request.user,
    #             context={'request': request}
    #         )
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     serializer = CustomUserSerializer(
    #         request.user,
    #         data=request.data,
    #         partial=True,
    #         context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

