from django.urls import path

from src.timesheet.controllers.timesheet import TimesheetController

urlpatterns = [
    path('', TimesheetController.as_view({'post': 'process_timesheet_event'})),
    path('<uuid:user_id>/', TimesheetController.as_view({'get': 'get_timesheet_days'})),
]
