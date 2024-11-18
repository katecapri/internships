import os
import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.email.services.email_service import send_email
from src.email.serializers import EmailSerializer
from src.services.decorators import request_body

logger = logging.getLogger('app')


class EmailController(viewsets.ViewSet):
    serializer_classes = {
        "send_email": EmailSerializer,
    }

    @request_body(EmailSerializer)
    def send_email(self, request, send_email_data):
        try:
            if "EMAIL_CONSUMER_KEY" in request.headers.keys() and \
                    request.headers["EMAIL_CONSUMER_KEY"] == os.getenv("API_CONSUMER_KEY"):
                email_event_id = send_email_data["id"]
                email_to = send_email_data["emailTo"]
                content = send_email_data["emailContent"]
                result = send_email(email_event_id, email_to, content)
                if result:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    logger.error(f"Email to {email_to} not sent")
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)


