import logging

from rest_framework import serializers
from src.points_event.services.points_event_core import EventType
from src.points_event.services.points_event_repository import PointsEventRepository

logger = logging.getLogger('app')


class CreatePointsEventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    eventType = serializers.CharField()
    pointsValue = serializers.CharField()
    reason = serializers.CharField()
    ownerId = serializers.UUIDField()

    def validate_id(self, value):
        db = PointsEventRepository()
        existing_points_event = db.get_points_event_by_id(value)
        if existing_points_event:
            raise serializers.ValidationError("Points event with such id already exists")
        else:
            return value

    def validate_eventType(self, value):
        is_event_type_valid = value in list(EventType)
        if is_event_type_valid:
            return value
        else:
            raise serializers.ValidationError("Invalid event type")
