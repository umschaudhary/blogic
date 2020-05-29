from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.commons.utils.permission_classes import (
    ManagerPermission,
    IsOwnerOrManager,
)

class CommonActionPermissionMixin:

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrManager],
        'retrieve': [AllowAny],
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

