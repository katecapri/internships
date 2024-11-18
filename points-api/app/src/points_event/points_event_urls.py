from django.urls import path

from src.points_event.controllers.points_event import PointsEventController

urlpatterns = [
    path('', PointsEventController.as_view({'get': 'get_history_of_points', 'post': 'create_points_event'})),
    path('sum/', PointsEventController.as_view({'get': 'get_sum_of_points'})),
]
