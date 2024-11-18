from django.urls import path
from src.auth.controllers.auth import AuthController

urlpatterns = [
    path('signup/', AuthController.as_view({'post': 'signup'})),
    path('login/', AuthController.as_view({'post': 'login'})),
    path('csrf/', AuthController.as_view({'get': 'get_csrf_code'})),
    path('email/confirm/', AuthController.as_view({'post': 'verify_email'})),
    path('password/request/', AuthController.as_view({'post': 'request_password'})),
    path('password/reset/', AuthController.as_view({'post': 'reset_password'})),
    path('logout/', AuthController.as_view({'post': 'logout'})),
]
