from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.api.v1.serializers.user import UserSerializer
from apps.api.v1.mixins.viewset import CreateListRetrieveUpdateViewSet
from apps.commons.utils.permission_classes import (
    ManagerPermission,
    IsOwnerOrManager,
)

User = get_user_model()


class UserViewSet(CreateListRetrieveUpdateViewSet):
    """
    list, create, update and retrieve viewset for Users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['phone_number', 'full_name', ]
    ordering_fields = (
        'created_at',
        'modified_at',
    )
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [ManagerPermission],
        'update': [IsOwnerOrManager],
        'retrieve': [IsAuthenticated],
        'partial_update': [IsOwnerOrManager]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
