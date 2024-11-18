from django.urls import path

from src.route.controllers.route import RouteController, DownloadTimesheetController

urlpatterns = [
    path('', RouteController.as_view({'get': 'get_routes'})),
    path('<uuid:pk>/request/', RouteController.as_view({'get': 'get_requests'})),
    path('<uuid:pk>/user/<slug:group_code>/', RouteController.as_view({'get': 'get_users'})),
    path('<uuid:pk>/timesheet/', RouteController.as_view({'get': 'get_timesheet_days',
                                                          'post': 'set_timesheet_days'})),
    path('<uuid:pk>/timesheet/download/', DownloadTimesheetController.as_view({'get': 'download_timesheet'})),
]
