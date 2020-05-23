from django.contrib.auth import get_user_model, logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.users.api.v1.serializers.user import (
    UserSerializer,
    PasswordChangeSerializer,
    PasswordSetSerializer
)
from apps.users.api.v1.utils.auth import get_jwt_token_response
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
        """ Permission setup """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_object(self):
        """ user detail """
        return self.request.user

    @action(
        detail=False,
        methods=['get', ],
        queryset=User.objects.all(),
        permission_classes=[IsAuthenticated],
        url_path="me",
        url_name="me"

    )
    def me(self, request, *args, **kwargs):
        """ User profile view """
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=['POST', ],
        detail=False,
        url_path='logout',
        url_name='logout'
    )
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)


class UserPasswordChangeView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class UserPasswordSetAPIView(UpdateAPIView):
    serializer_class = PasswordSetSerializer
    queryset = User.objects.filter(
        is_blocked=False,
        is_active=True
    )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        phone_number = self.request.data.get('phone_number')

        obj = get_object_or_404(queryset, phone_number=phone_number)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return get_jwt_token_response(login_data=serializer.data)
