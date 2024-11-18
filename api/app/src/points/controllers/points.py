import logging
import os
import requests

from rest_framework import viewsets, status
from rest_framework.response import Response

logger = logging.getLogger('app')


class PointsController(viewsets.ViewSet):
    serializer_classes = {
        "get_sum_of_points": None,
        "get_history_of_points": None,
    }

    def get_sum_of_points(self, request, pk):
        try:
            url = f'{os.getenv("POINTS_URL")}/api/v1/points/sum/'
            params = dict()
            for key in request.GET.keys():
                params[key] = request.GET[key]
            params["userId"] = str(pk)
            result = requests.get(url, params=params)
            return Response(data=result.text,
                            status=result.status_code)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_history_of_points(self, request, pk):
        try:
            url = f'{os.getenv("POINTS_URL")}/api/v1/points/'
            params = dict()
            for key in request.GET.keys():
                params[key] = request.GET[key]
            params["userId"] = str(pk)
            result = requests.get(url, params=params)
            return Response(data=result.json(),
                            status=result.status_code)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
