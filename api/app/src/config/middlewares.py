import logging
import os

import jwt
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from src.user.services.user_service import get_user_by_id
from src.app_role.services.app_role_service import get_app_role_uuid_by_code, get_app_role_permission_by_attrs, \
    get_permission_rule
from src.app_role.services.app_role_core import AppRolePermissionLevel

logger = logging.getLogger('app')


def get_401_response():
    response = Response(status=status.HTTP_401_UNAUTHORIZED)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if not hasattr(request, "session"):
                raise ImproperlyConfigured(
                    "The AuthMiddleware middleware requires session middleware to "
                    "be installed. Edit your MIDDLEWARE setting to insert "
                    "'django.contrib.sessions.middleware.SessionMiddleware' before "
                    "'config.middlewares.AuthMiddleware'."
                )
            jwt_token = request.session.get('jwt', None)
            if jwt_token:
                if "Authorization" in request.headers.keys():
                    incoming_token = request.headers['Authorization']
                    if incoming_token[incoming_token.find("Bearer") + 7:] == jwt_token:
                        decoded = jwt.decode(jwt_token, os.getenv("API_JWT_SECRET"),
                                             algorithms=[os.getenv("API_JWT_ALGORITHM")])
                        user = get_user_by_id(decoded["sub"])
                        if user:
                            request.hackathonUser = user
        except Exception as e:
            logger.error(e, exc_info=True)


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if "API_CONSUMER_KEY" in request.headers \
                and request.headers["API_CONSUMER_KEY"] == os.getenv("API_CONSUMER_KEY"):
            return
        if hasattr(request, "hackathonUser"):
            user_app_role_id = request.hackathonUser.app_role_id
        else:
            user_app_role_id = get_app_role_uuid_by_code("APP_USER")
        method = request.method
        path = request.path
        if path.startswith("/api/v1"):
            path = path[7:]

        if path.startswith("/auth"):
            return
        if "timesheet" in path and method == "POST":
            return
        if "Referer" not in request.headers.keys():
            logging.error("Referer missing in headers")
            return get_401_response()

        if "admin" in request.headers["Referer"]:
            app_role_permission = get_app_role_permission_by_attrs(
                AppRolePermissionLevel.COMPONENT, "admin_console")
        elif "cabinet" in request.headers["Referer"]:
            app_role_permission = get_app_role_permission_by_attrs(
                AppRolePermissionLevel.COMPONENT, "cabinet")
        else:
            logging.error("Failed to determine the url to grant access")
            return get_401_response()

        permission_component_rule = get_permission_rule(app_role_id=user_app_role_id,
                                                        app_role_permission_id=app_role_permission.id)

        if bool(permission_component_rule.has_access) is False:
            logging.error("User doesn't have access to the component")
            return get_401_response()

        entry_point = "/" + path.split('/')[1]
        app_role_permission = get_app_role_permission_by_attrs(
            AppRolePermissionLevel.BUSINESS_OBJECT, entry_point)
        if not app_role_permission:
            logging.error("App role permission with such entry point doesn't exists")
            return get_401_response()
        permission_rule = get_permission_rule(app_role_id=user_app_role_id,
                                              app_role_permission_id=app_role_permission.id)
        if not permission_rule:
            logging.error("App role permission rule doesn't exists")
            return get_401_response()
        if method == "GET":
            if bool(permission_rule.read_permission or permission_rule.view_all_permission) is True:
                return
        else:
            if path == app_role_permission.entry_point + '/':
                if bool(permission_rule.create_permission) is True:
                    return
            else:
                if method == "DELETE":
                    if bool(permission_rule.delete_permission or permission_rule.modify_all_permission) is True:
                        return
                else:  # if method in ["POST", "PATCH"]:
                    if bool(permission_rule.update_permission or permission_rule.modify_all_permission) is True:
                        return
        logging.error("User doesn't have access to the method")
        return get_401_response()
