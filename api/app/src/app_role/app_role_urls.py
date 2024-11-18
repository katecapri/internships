from django.urls import path

from src.app_role.controllers.app_role import AppRoleController

urlpatterns = [
    path('', AppRoleController.as_view({'get': 'get_app_roles', 'post': 'create_app_role'})),
    path('<uuid:pk>/', AppRoleController.as_view({'post': 'update_app_role', 'delete': 'delete_app_role'})),
]
