from django.urls import path

from src.route.controllers.request import RequestController

urlpatterns = [
    path('', RequestController.as_view({'get': 'read_user_requests', 'post': 'create_request'})),
    path('<uuid:pk>/verify/', RequestController.as_view({'post': 'verify_request'})),
    path('<uuid:pk>/verificationStatus/', RequestController.as_view({'get': 'get_request_status'})),
]
