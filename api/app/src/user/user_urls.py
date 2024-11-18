from django.urls import path

from src.user.controllers.user import UserController

urlpatterns = [
    path('', UserController.as_view({'get': 'get_users', 'post': 'create_user'})),
    path('current/', UserController.as_view({'get': 'read_current_user'})),
    path('<uuid:pk>/', UserController.as_view({'get': 'read_user', 'post': 'update_user', "delete": "delete_user"})),
]
