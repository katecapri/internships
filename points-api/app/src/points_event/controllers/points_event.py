import logging
import os

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.points_event.services.points_event_service import get_points_events_for_user, \
    get_sum_of_points_for_user, create_points_event
from src.points_event.services.points_event_core import EventType
from src.points_event.serializers import CreatePointsEventSerializer
from src.services.decorators import request_body

logger = logging.getLogger('app')


class PointsEventController(viewsets.ViewSet):
    serializer_classes = {
        "get_history_of_points": None,
        "create_points_event": CreatePointsEventSerializer,
        "get_sum_of_points": None,
    }

    def get_history_of_points(self, request):
        try:
            input_params = request.GET.keys()
            if "userId" not in input_params:
                logger.error("Required userId parameter is missing")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user_id = request.GET["userId"]
            offset = int(request.GET["offset"]) if "offset" in input_params else 1
            limit = int(request.GET["limit"]) if "limit" in input_params else 5
            result = get_points_events_for_user(user_id, offset, limit)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(CreatePointsEventSerializer)
    def create_points_event(self, request, create_points_event_data):
        try:
            if "POINTS_CONSUMER_KEY" in request.headers.keys() and \
                    request.headers["POINTS_CONSUMER_KEY"] == os.getenv("API_CONSUMER_KEY"):
                current_sum_of_user_points = get_sum_of_points_for_user(create_points_event_data["ownerId"])
                if create_points_event_data["eventType"] == EventType.DECREASE and \
                        current_sum_of_user_points - float(create_points_event_data["pointsValue"]) < 0:
                    logger.info("Points decrease denied. The sum cannot be less than zero.")
                    return Response(status=status.HTTP_200_OK)
                result = create_points_event(create_points_event_data)
                if result:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    logger.error("Points event was not created")
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_sum_of_points(self, request):
        try:
            if "userId" not in request.GET.keys():
                logger.error("Required userId parameter is missing")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = get_sum_of_points_for_user(request.GET["userId"])
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

