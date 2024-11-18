import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.user.services.user_service import get_users, create_user, update_user, get_user_by_id, delete_user, \
    convert_user_to_representation, check_user_can_use_method, check_new_role_and_groups_are_valid
from src.user.services.user_core import CreateUserData
from src.user.serializers import CreateUserSerializer, UpdateUserSerializer, available_groups_for_roles
from src.auth.services.auth_service import request_password
from src.services.decorators import request_body

logger = logging.getLogger('app')


class UserController(viewsets.ViewSet):
    serializer_classes = {
        "get_users": None,
        "create_user": CreateUserSerializer,
        "read_current_user": None,
        "read_user": None,
        "update_user": UpdateUserSerializer,
        "delete_user": None,
    }

    def get_users(self, request):
        try:
            users = get_users()
            result = [convert_user_to_representation(user[0]) for user in users]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(CreateUserSerializer)
    def create_user(self, request, create_user_data):
        try:
            new_user_info = CreateUserData(
                email=create_user_data["email"],
                name=create_user_data["name"],
                is_email_confirmed=True,
                app_role_id=create_user_data["appRoleId"],
                groups=create_user_data["groups"],
            )
            result = create_user(new_user_info)
            request_password(create_user_data["email"])
            if result:
                return Response(status=status.HTTP_201_CREATED)
            else:
                logger.error("User was not created")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def read_current_user(self, request):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = get_user_by_id(request.hackathonUser.id)
            result = convert_user_to_representation(user)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def read_user(self, request, pk):
        try:
            user = get_user_by_id(pk)
            if not user:
                logger.error('User with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_user_to_representation(user)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(UpdateUserSerializer)
    def update_user(self, request, data_to_update_user, pk):
        try:
            if not check_user_can_use_method(request, pk):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if data_to_update_user["appRoleId"] and request.hackathonUser.app_role.code != "ADMIN":
                logger.error('Only admin can change user role')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = get_user_by_id(pk)
            if not user:
                logger.error('User with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not check_new_role_and_groups_are_valid(user, data_to_update_user, available_groups_for_roles):
                logger.error('The user update isn`t correct because groups don`t match for the app role')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = update_user(pk, data_to_update_user)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error('User was not updated')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete_user(self, request, pk):
        try:
            if not check_user_can_use_method(request, pk):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = get_user_by_id(pk)
            if user and user.app_role.code == "ADMIN" and request.hackathonUser.app_role.code != "ADMIN":
                return Response(status=status.HTTP_200_OK)
            delete_user(pk)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
