from rest_framework import viewsets, status
from rest_framework.response import Response


class TestController(viewsets.ViewSet):
    serializer_classes = {
        "get_result": None,
    }

    def get_result(self, request):
        return Response(data={"result": "Hackaton2023-backend"}, status=status.HTTP_200_OK)
