from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.db.models.expressions import Value
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, SubscribeSerializer,
                             TagSerializer, TokenSerializer,
                             UserCreateSerializer, UserListSerializer,
                             UserPasswordSerializer)

User = get_user_model()


class AddAndDeleteSubscribe(
        generics.RetrieveDestroyAPIView,
        generics.ListCreateAPIView
):
    """Подписка и отписка от пользователя."""

    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.follower.select_related(
            'following'
        ).prefetch_related(
            'following__recipe'
        ).annotate(
            recipes_count=Count('following__recipe'),
            is_subscribed=Value(True), )

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(self.request, user)
        return user

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        subs = request.user.follower.create(author=instance)
        serializer = self.get_serializer(subs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.follower.filter(author=instance).delete()
