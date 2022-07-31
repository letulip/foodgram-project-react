from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractUser):
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


# vpupkin token
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1OTI4MzgxOSwianRpIjoiMGI3YzQwYzM0YmRiNGY0YThiZDFhZTU2ZDhkZGQ2ZmUiLCJ1c2VyX2lkIjoyfQ.Mijei7QOKHjF5XuRe0wCdyzTcFZlsV28rcBUJD136d4",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3ODM3NDE5LCJqdGkiOiI4MGJlYzVmYjU5M2Y0MDExYWI4ZGIwNmYxMjI4NzNlZSIsInVzZXJfaWQiOjJ9.XBL0TLUHPo2Tn0mUeRWZGJufbqPezy6uNAl9HqcqTcM"
# }

# vpupkin2 token
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1OTI4NDE2MCwianRpIjoiM2Q2NTZiNzRlZmZmNGQ4Yzk5Y2Q5MjgyZjA4NWY5NTgiLCJ1c2VyX2lkIjozfQ.y8JzrwFIo9IhHp79zh84iHhgvY7A0DrMVsdSEBrI23o",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3ODM3NzYwLCJqdGkiOiJlOWY0ODQ0NzYwMjA0MjFmYmYyZWRlMWFjN2NkZjI5MSIsInVzZXJfaWQiOjN9.Hoi49t3R_EZ5XA7x11k53W9k7fYUWFS7P60f1_MdvjQ"
# }