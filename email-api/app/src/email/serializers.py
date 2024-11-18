import logging

from rest_framework import serializers
from src.email.services.email_repository import EmailRepository

logger = logging.getLogger('app')


class EmailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    emailContent = serializers.CharField()
    emailTo = serializers.EmailField()

    def validate_id(self, value):
        db = EmailRepository()
        existing_email_event = db.get_email_event_by_id(value)
        if existing_email_event:
            raise serializers.ValidationError("Email event with such id already exists")
        else:
            return value
