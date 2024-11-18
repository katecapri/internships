import logging
import requests
import os
from datetime import datetime
import shutil
import tempfile

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer

from src.route.services.route_service import get_routes, convert_route_to_representation, \
    get_route_step_by_id, convert_request_for_route, get_requests_by_route_step_id, get_route_by_id
from src.user.services.user_service import get_trainees_by_route_id
from src.route.serializers import SetTimesheetDaySerializer
from src.route.services.timesheet_service import check_timesheet_day_belongs_to_user, \
    prepare_info_to_update_timesheet_day, export_timesheet_as_excel
from src.services.permission_service import EntryPoint, PermissionType, has_user_permission
from src.services.decorators import request_body

from src.controllers_abstractions import Controller


logger = logging.getLogger('app')


class RouteController(viewsets.ViewSet):
    serializer_classes = {
        "get_routes": None,
        "get_requests": None,
        "get_users": None,
        "get_timesheet_days": None,
        "set_timesheet_days": SetTimesheetDaySerializer,
    }

    def get_routes(self, request):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            routes = get_routes(request.hackathonUser)
            result = [convert_route_to_representation(route) for route in routes]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_requests(self, request, pk):
        try:
            if "routeStepId" not in request.GET.keys():
                return Response(data=[], status=status.HTTP_200_OK)
            route_step_id = request.GET["routeStepId"]
            route_step = get_route_step_by_id(route_step_id)
            if route_step.route_id != pk:
                logger.error('The route step doesn`t belong to the route')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            requests = get_requests_by_route_step_id(route_step_id)
            result = [convert_request_for_route(request) for request in requests]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_users(self, request, pk, group_code):
        try:
            route = get_route_by_id(pk)
            if route.from_group == group_code == 'trainee':
                trainees = get_trainees_by_route_id(pk)
                result = [
                    {
                        "id": trainee.user.id,
                        "email": trainee.user.email,
                        "name": trainee.user.name,
                    } for trainee in trainees
                ]
            else:
                result = []
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_timesheet_days(self, request, pk):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if "userId" not in request.GET.keys():
                user_id = request.hackathonUser.id
            else:
                user_id = request.GET["userId"]
                if user_id != request.hackathonUser.id:
                    can_user_view_all = has_user_permission(
                        request.hackathonUser.app_role, PermissionType.VIEW_ALL, EntryPoint.ROUTE)
                    if not can_user_view_all:
                        logger.error('User app role doesn`t allow reading information about other users')
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
            url = f'{os.getenv("TIMESHEET_URL")}/api/v1/timesheet/{user_id}/'
            result = requests.get(url, params={"routeId": pk})
            return Response(data=result.json(), status=result.status_code)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(SetTimesheetDaySerializer)
    def set_timesheet_days(self, request, update_timesheet_day_data, pk):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if "userId" not in request.GET.keys():
                user_id = request.hackathonUser.id
            else:
                user_id = request.GET["userId"]
                if user_id != request.hackathonUser.id:
                    can_user_modify_all = has_user_permission(
                        request.hackathonUser.app_role, PermissionType.MODIFY_ALL, EntryPoint.ROUTE)
                    if not can_user_modify_all:
                        logger.error('User app role doesn`t allow changing information about other users')
                        return Response(status=status.HTTP_401_UNAUTHORIZED)

            timesheet_day_id = update_timesheet_day_data["id"]
            timesheet_date = update_timesheet_day_data["timeSheetDate"]
            is_user_timesheet_day = check_timesheet_day_belongs_to_user(user_id, pk, timesheet_day_id, timesheet_date)
            if not is_user_timesheet_day:
                logger.error('User has no such timesheet day for updating')
                return Response(status=status.HTTP_400_BAD_REQUEST)

            day_type = update_timesheet_day_data["dayType"]
            update_info = prepare_info_to_update_timesheet_day(user_id, pk, timesheet_date, day_type)
            url = f'{os.getenv("TIMESHEET_URL")}/api/v1/timesheet/'
            result = requests.post(url, json=update_info)
            return Response(status=result.status_code)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DownloadTimesheetController(Controller):
    class XLSXRenderer(BaseRenderer):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        format = "xlsx"
        charset = None
        render_style = "binary"

        def render(self, data, media_type=None, renderer_context=None):
            return data

    renderer_classes = [XLSXRenderer]
    serializer_classes = {
        "download_timesheet": None
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def download_timesheet(self, request, pk):
        try:
            route = get_route_by_id(pk)
            if datetime.now().date() < route.start_date:
                logger.error("The internship hasn't started yet")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            filename = f"{str(pk)}.xlsx"
            tempdir = tempfile.mkdtemp(prefix=str(pk), dir="/")
            filepath = os.path.join(tempdir, filename)
            shutil.copy2('/application/media/timesheet_template_top_part.xlsx', filepath)
            export_timesheet_as_excel(filepath, route)
            with open(filepath, 'rb') as file:
                response = Response(file.read(), headers={
                    'Content-Disposition': 'attachment; '
                                           f'filename="{filename}"'
                })
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
