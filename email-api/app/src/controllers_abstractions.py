from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class Controller(viewsets.ModelViewSet):
    serializer_classes = dict[str, Serializer]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields: list[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def send(data, message: str) -> Response:
        return Response(data, status=status.HTTP_200_OK)

