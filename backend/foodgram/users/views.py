# from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import HttpRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.permissions import IsAdminOrReadOnly
from .models import User, Subscriptions
from .serializers import UsersSerializer, UserSelfSerializer, SubscriptionsSerializer
from .pagination import CustomPagination


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        '^username',
        '$username'
    )
    # lookup_field = 'username'

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_account_information(self, request):
        user = get_object_or_404(User, username=request.user)

        if request.method == 'GET':
            serializer = UsersSerializer(user)
            return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=(IsAuthenticated,),
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

    def post(self, request: HttpRequest):
        if not request.data or 'email' not in request.data:
            return Response(status=HTTP_400_BAD_REQUEST)

        email = request.data['email']
        user = get_object_or_404(User, email=email)
        password = request.data['password']
        if user.check_password(password):
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


class SubscriptionsViewSet(ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


class SubscribeViewSet(ModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(User, pk=author_id)
        return author.follower.all()

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(User, pk=author_id)
        data = {
            'user': request.user.id,
            'author': author_id
        }
        context = {
            'request': request
        }
        serializer = self.get_serializer(data=data, context=context)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            serializer.save(user=request.user, author=author)
        except IntegrityError:
            message = {
                'unique_together': 'Author already in your subscriptions',
            }
            return Response(
                data=message,
                status=HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTP_200_OK,
            headers=headers
        )
