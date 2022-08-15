from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Subscription, User
from .pagination import CustomPagination
from .serializers import (SubscriptionSerializer, UserSelfSerializer,
                          UsersSerializer)


class UsersViewSet(ModelViewSet):
    """
    Отображение списка пользователей.
    Просмотр доступен всем пользователям.
    Редактирование доступно Администратору.
    """

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        '^username',
        '$username'
    )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_account_information(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
    )
    def post(self, request: HttpRequest):
        user = get_object_or_404(User, email=request.user.email)
        current_password = request.data['current_password']
        if user.check_password(current_password):
            user.set_password(request.data['new_password'])
            serializer = UserSelfSerializer(
                user,
                data=user.__dict__
            )
            if serializer.is_valid():
                serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)
        data = {
            'password': 'wrong password',
        }
        return Response(data=data, status=HTTP_400_BAD_REQUEST)


class UserKeyView(ObtainAuthToken):
    """
    Получение ключа аутентификации - логин.
    Доступно всем пользователям.
    """

    def post(self, request: HttpRequest):
        if not request.data or 'email' not in request.data:
            return Response(status=HTTP_400_BAD_REQUEST)

        email = request.data['email']
        user = get_object_or_404(User, email=email)
        password = request.data['password']
        if user.check_password(password):
            existing_token = Token.objects.filter(user=user)
            if existing_token:
                existing_token.delete()
            auth_token = Token.objects.create(user=user)
            token = {
                'auth_token': auth_token.key
            }
            return Response(data=token, status=HTTP_200_OK)
        data = {
            'password': 'wrong password',
        }
        return Response(data=data, status=HTTP_400_BAD_REQUEST)


class UserKeyDeleteView(APIView):
    """
    Удаление ключа аутентификации - логаут.
    Доступно только авторизованным пользователям.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request: HttpRequest):
        try:
            request.user.auth_token.delete()
            data = {
                "message": "You have successfully logged out.",
            }
            return Response(data, status=HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=HTTP_401_UNAUTHORIZED)


class SubscriptionViewSet(ModelViewSet):
    """
    Отображение списка подписок пользователя.
    Доступно только авторизованным пользователям.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(follower__user=self.request.user)


class SubscribeViewSet(ModelViewSet):
    """
    Создание и удаление подписки на автора.
    Доступно только авторизованным пользователям.
    """
    
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(User, pk=author_id)
        return author.following.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(User, pk=author_id)
        if user == author:
            return Response(
                {
                    'error': 'No self subscription'
                },
                status=HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
            user=user,
            author_id=author_id
        ).exists():
            return Response(
                {
                    'error': 'You already subscribed to this user'
                },
                status=HTTP_400_BAD_REQUEST
            )
        Subscription.objects.create(
            user=user,
            author_id=author_id
        )
        context = {
            'request': request
        }
        serializer = self.serializer_class(author, context=context)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        subscribed = Subscription.objects.filter(
            user=request.user,
            author_id=author_id
        )
        if subscribed:
            subscribed.delete()
            return Response(
                status=HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                'error': 'You were not subscribed to this user'
            },
            status=HTTP_400_BAD_REQUEST
        )
