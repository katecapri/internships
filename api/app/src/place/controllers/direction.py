import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.place.services.place_service import get_directions, get_direction_by_id, \
    convert_direction_to_representation, update_direction
from src.place.serializers import UpdateDirectionSerializer
from src.services.decorators import request_body

logger = logging.getLogger('app')


class DirectionController(viewsets.ViewSet):
    serializer_classes = {
        "get_directions": None,
        "get_direction": None,
        "update_direction": UpdateDirectionSerializer,
    }

    def get_directions(self, request):
        try:
            directions = get_directions()
            result = [convert_direction_to_representation(direction) for direction in directions]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_direction(self, request, pk):
        try:
            direction = get_direction_by_id(pk)
            if not direction:
                logger.error('Direction with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_direction_to_representation(direction)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(UpdateDirectionSerializer)
    def update_direction(self, request, data_to_update_direction, pk):
        try:
            direction = get_direction_by_id(pk)
            if not direction:
                logger.error('Direction with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not any([data_to_update_direction["name"], data_to_update_direction["display"],
                        data_to_update_direction["departments"] is not None]):
                logger.error('One of the fields must be filled')
                return Response(status=status.HTTP_400_BAD_REQUEST)

            result = update_direction(pk, data_to_update_direction)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error('Direction was not updated')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
