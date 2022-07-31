from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UsersSerializer, UserSelfSerializer, UserKeySerializer
from .pagination import CustomPagination


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # todo permission_classes = (IsAdminOrReadOnly,)
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
            print(self.__dict__)
            print()
            print(request.__dict__)
            # print('Bearer %s' % self.GetAccessToken().token)
            return Response(serializer.data)

        # if request.method == 'PATCH':
        #     if request.user.role == 'admin':
        #         serializer = UsersSerializer(user, data=request.data)
        #     else:
        #         serializer = UserSelfSerializer(user, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #     return Response(serializer.data, status=HTTP_200_OK)
        # return False

    @action(
        methods=['post'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='set_password',
    )
    def post(self, request: HttpRequest):
        user = get_object_or_404(User, email=request.user.email)
        current_password = request.data['current_password']
        # if user.password == current_password:
        print('time to check password', request.data['current_password'])
        if user.check_password(current_password):
            # user.password = request.data['new_password']
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


# from django.views.decorators.csrf import csrf_protect

class UserKeyView(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = UserKeySerializer

    # @csrf_protect
    def post(self, request: HttpRequest):
        if not request.data or 'email' not in request.data:
            return Response(status=HTTP_400_BAD_REQUEST)

        email = request.data['email']
        user = get_object_or_404(User, email=email)
        password = request.data['password']
        # if user.password == password:
        if user.check_password(password):
        # if (get_check_hash.check_token(user=user, token=code)):
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh_token': str(refresh),
                'auth_token': str(refresh.access_token),
            }
            return Response(data=token, status=HTTP_200_OK)
        data = {
            'password': 'wrong password',
        }
        return Response(data=data, status=HTTP_400_BAD_REQUEST)


class UserKeyDeleteView(APIView):
    # queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    # TODO

    def post(self, request: HttpRequest):
        print(request.auth.__dict__)
        print(request.auth_token.delete())
        try:
            print(request.auth.token)
            request.auth.token = None
            request.user.auth_token.delete()
            data = {
                "message": "You have successfully logged out.",
            }
            print(request.auth.token)
            print(request.auth.__dict__)
            print(datetime.utcnow().strftime('%s'))
            return Response(data, status=HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=HTTP_401_UNAUTHORIZED)
