from django.urls import path

from src.place.controllers.direction import DirectionController

urlpatterns = [
    path('', DirectionController.as_view({'get': 'get_directions'})),
    path('<uuid:pk>/', DirectionController.as_view({'get': 'get_direction', 'post': 'update_direction'})),
]
