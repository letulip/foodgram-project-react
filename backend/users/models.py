from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-_]+$',
                message="""This value may contain only letters,
                digits and @/./+/-/_ characters."""
            ),
            RegexValidator(
                regex=r'^\b(m|M)e\b',
                inverse_match=True,
                message="""Username Me registration not allowed."""
            )
        ],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email address'
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    password = models.CharField(
        max_length=150,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.username


class Subscriptions(models.Model):
    """
    Модель подписок.
    """

    user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )

    class Meta():
        unique_together = [
            ('user', 'author',)
        ]

    def __str__(self) -> str:
        full_name = f'{self.author} добавлен в подписки {self.user}'
        return full_name