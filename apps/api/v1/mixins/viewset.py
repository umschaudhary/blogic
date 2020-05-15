from django.utils.functional import cached_property
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    RetrieveModelMixin, ListModelMixin,
    UpdateModelMixin, CreateModelMixin,
    DestroyModelMixin
)

from rest_framework.viewsets import GenericViewSet


class BaseViewSet(GenericViewSet):
    """"
    :cvar serializer_include_fields:
        fields to include in serializer

        type -->  iterable

        set this value or override get_serializer_include_fields

    :cvar serializer_exclude_fields:
        fields to exclude in serializer

        type -->  iterable

        set this value or override get_serializer_exclude_fields

    """
    serializer_include_fields = None
    serializer_exclude_fields = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        kwargs['fields'] = self.get_serializer_include_fields()
        kwargs['exclude_fields'] = self.get_serializer_exclude_fields()
        return serializer_class(*args, **kwargs)

    def get_serializer_include_fields(self):
        return self.serializer_include_fields

    def get_serializer_exclude_fields(self):
        return self.serializer_exclude_fields


class ListViewSet(ListModelMixin, BaseViewSet):
    pass


class CreateViewSet(CreateModelMixin, BaseViewSet):
    pass


class RetrieveViewSet(RetrieveModelMixin, BaseViewSet):
    pass


class UpdateViewSet(UpdateModelMixin, BaseViewSet):
    pass


class DestroyViewSet(DestroyModelMixin, BaseViewSet):
    pass


class ReadOnlyViewSet(ListViewSet, RetrieveViewSet):
    pass


class CreateRetrieveViewSet(CreateViewSet, RetrieveViewSet):
    pass


class RetrieveUpdateViewSet(UpdateViewSet, RetrieveViewSet):
    pass


class ListRetrieveUpdateViewSet(ListViewSet,
                                RetrieveViewSet, UpdateViewSet):
    pass


class CreateListViewSet(CreateViewSet, ListViewSet):
    pass


class CreateListRetrieveViewSet(CreateViewSet, ListViewSet, RetrieveViewSet):
    pass


class CreateRetrieveUpdateViewSet(CreateViewSet,
                                  RetrieveViewSet, UpdateViewSet):
    pass


class CreateListRetrieveUpdateViewSet(CreateViewSet,
                                      ListViewSet,
                                      RetrieveViewSet,
                                      UpdateViewSet):
    pass


class CreateListDestroyViewSetMixin(CreateViewSet,
                                    ListViewSet, DestroyViewSet):
    pass


class CustomModelViewSet(CreateViewSet,
                         ListViewSet,
                         RetrieveUpdateViewSet,
                         DestroyViewSet):
    pass
