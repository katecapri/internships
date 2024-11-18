import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.place.serializers import CreatePlaceSerializer, UpdatePlaceSerializer
from src.place.services.place_service import get_places, create_place, get_place_by_id, \
    update_place, delete_place, convert_place_to_representation
from src.user.services.user_service import check_user_manager_or_admin
from src.services.decorators import request_body

logger = logging.getLogger('app')


class PlaceController(viewsets.ViewSet):
    serializer_classes = {
        "get_places": None,
        "create_place": CreatePlaceSerializer,
        "read_place": None,
        'update_place': UpdatePlaceSerializer,
        "delete_place": None,
    }

    def get_places(self, request):
        try:
            places = get_places()
            result = [convert_place_to_representation(place) for place in places]
            if result:
                return Response(result, status.HTTP_200_OK)
            else:
                logging.error("No places to response")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(CreatePlaceSerializer)
    def create_place(self, request, create_place_data):
        try:
            new_place = create_place(create_place_data)
            if not new_place:
                logger.error('Place was not created')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_place_to_representation(new_place)
            return Response(data=result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def read_place(self, request, pk):
        try:
            place = get_place_by_id(pk)
            if not place:
                logger.error('Place with such id doesn`t exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_place_to_representation(place)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(UpdatePlaceSerializer)
    def update_place(self, request, update_place_data, pk):
        try:
            if not check_user_manager_or_admin(request):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            place = get_place_by_id(pk)
            if not place:
                logger.error('Place with such id doesn`t exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not any([update_place_data["name"], update_place_data["address"],
                        update_place_data["departments"] is not None]):
                logger.error('One of the fields must be filled')
                return Response(status=status.HTTP_400_BAD_REQUEST)

            place = update_place(pk, update_place_data)
            if place:
                result = convert_place_to_representation(place)
                return Response(data=result, status=status.HTTP_200_OK)
            else:
                logger.error("Place was not updated")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete_place(self, request, pk):
        try:
            if not check_user_manager_or_admin(request):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            place = get_place_by_id(pk)
            if not place:
                logging.error("Place with such id doesn`t exist")
                return Response(status=status.HTTP_200_OK)

            result = delete_place(pk)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error("Place was not deleted")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
