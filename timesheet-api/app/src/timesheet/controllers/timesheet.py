import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.timesheet.services.timesheet_service import generate_or_update_timesheet, \
    get_timesheet_days_by_user_and_route, get_timesheet_event_by_id, close_timesheet_event
from src.timesheet.serializers import ProcessTimesheetEventSerializer
from src.services.decorators import request_body

logger = logging.getLogger('app')


class TimesheetController(viewsets.ViewSet):
    serializer_classes = {
        "process_timesheet_event": ProcessTimesheetEventSerializer,
        "get_timesheet_days": None,
    }

    @request_body(ProcessTimesheetEventSerializer)
    def process_timesheet_event(self, request, timesheet_event_data):
        try:
            result = generate_or_update_timesheet(timesheet_event_data)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error("Timesheet event was not created or was interrupted")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            event = get_timesheet_event_by_id(timesheet_event_data["eventId"])
            if event and not event.end_date:
                close_timesheet_event(event_id=timesheet_event_data["eventId"], is_interrupted=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_timesheet_days(self, request, user_id):
        try:
            if "routeId" not in request.GET.keys():
                logger.error("Required routeId parameter is missing")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            route_id = request.GET["routeId"]
            result = get_timesheet_days_by_user_and_route(user_id, route_id)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)


