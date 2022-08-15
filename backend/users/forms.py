from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Форма создания нового пользователя.
    """

    class Meta:
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Форма смены пароля пользователя.
    """

    class Meta:
        model = User
        fields = ('username', 'email',)
