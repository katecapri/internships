from django.urls import path

from src.email.controllers.email import EmailController

urlpatterns = [
    path('', EmailController.as_view({'post': 'send_email'})),
]
