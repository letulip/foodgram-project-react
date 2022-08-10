from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Subscriptions
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', ]

admin.site.register(User, CustomAdmin)
admin.site.register(Subscriptions)
