from django.urls import path

from src.place.controllers.place import PlaceController

urlpatterns = [
    path('', PlaceController.as_view({'get': 'get_places', 'post': 'create_place'})),
    path('<uuid:pk>/', PlaceController.as_view({'get': 'read_place', 'post': 'update_place', 'delete': 'delete_place'})),
]
