from django.urls import path

from src.points.controllers.points import PointsController

urlpatterns = [
    path('<uuid:pk>/sum/', PointsController.as_view({'get': 'get_sum_of_points'})),
    path('<uuid:pk>/history/', PointsController.as_view({'get': 'get_history_of_points'})),
]
