from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscribe


EMPTY_MSG = '-пусто-'
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', 'date_joined',)
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('date_joined', 'email', 'first_name')
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author', 'created',)
    search_fields = (
        'user__email', 'author__email',)
    empty_value_display = EMPTY_MSG
