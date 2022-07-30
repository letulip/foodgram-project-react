from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UsersSerializer
from .pagination import CustomPagination


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
