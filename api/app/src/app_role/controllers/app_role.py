import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.app_role.serializers import AppRoleSerializer
from src.app_role.services.app_role_service import get_app_roles, get_app_role_by_id, \
    create_app_role, update_app_role, delete_app_role
from src.user.services.user_service import check_app_role_belongs_to_user
from src.services.decorators import request_body

logger = logging.getLogger('app')


class AppRoleController(viewsets.ViewSet):
    serializer_classes = {
        "get_app_roles": None,
        "create_app_role": AppRoleSerializer,
        'update_app_role': AppRoleSerializer,
        "delete_app_role": None,
    }

    def get_app_roles(self, request):
        try:
            result = get_app_roles()
            if result:
                return Response(result, status.HTTP_200_OK)
            else:
                logging.error("No app roles to response")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(AppRoleSerializer)
    def create_app_role(self, request, create_app_role_data):
        try:
            result = create_app_role(create_app_role_data)
            if result:
                return Response(result, status.HTTP_201_CREATED)
            else:
                logger.error("App role was not created")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(AppRoleSerializer)
    def update_app_role(self, request, update_app_role_data, pk):
        try:
            result = update_app_role(update_app_role_data, pk)
            if result:
                return Response(result, status.HTTP_200_OK)
            else:
                logger.error("App role was not updated")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete_app_role(self, request, pk):
        try:
            is_app_role_used = check_app_role_belongs_to_user(pk)
            if is_app_role_used:
                logger.error("App role was not deleted")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            app_role = get_app_role_by_id(pk)
            if not app_role:
                logging.error("App role with such id doesn`t exist")
                return Response(status=status.HTTP_200_OK)
            if app_role.code in ("GUEST", "ADMIN"):
                logging.error("Guest or administrator role not removed")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = delete_app_role(pk)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error("App role was not deleted")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
