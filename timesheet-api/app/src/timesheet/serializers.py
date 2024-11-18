import logging

from rest_framework import serializers
from src.timesheet.services.timesheet_core import EventType, DayType, DurationItem
from src.timesheet.services.timesheet_service import get_timesheet_event_by_id

logger = logging.getLogger('app')


class GenerateTimesheetSerializer(serializers.Serializer):
    dateStart = serializers.CharField()
    duration = serializers.IntegerField()
    durationItem = serializers.CharField()

    def validate_durationItem(self, value):
        is_duration_item_valid = value in list(DurationItem)
        if is_duration_item_valid:
            return value
        else:
            raise serializers.ValidationError("Invalid duration item")


class UpdateTimesheetSerializer(serializers.Serializer):
    eventDate = serializers.CharField()
    dayType = serializers.CharField()

    def validate_dayType(self, value):
        is_day_type_valid = value in list(DayType)
        if is_day_type_valid:
            return value
        else:
            raise serializers.ValidationError("Invalid day type")


class ProcessTimesheetEventSerializer(serializers.Serializer):
    eventId = serializers.UUIDField()
    userId = serializers.UUIDField()
    routeId = serializers.UUIDField()
    eventType = serializers.CharField()
    toGenerate = GenerateTimesheetSerializer(allow_null=True, default=None)
    toUpdate = UpdateTimesheetSerializer(allow_null=True, default=None)

    def validate(self, data):
        try:
            event = get_timesheet_event_by_id(data["eventId"])
            if event:
                raise serializers.ValidationError("Timesheet event with such id already exists")
            if data["eventType"] == EventType.update:
                if not data["toUpdate"]:
                    raise serializers.ValidationError("No info to update")
            elif data["eventType"] == EventType.generate:
                if not data["toGenerate"]:
                    raise serializers.ValidationError("No info to generate")
            else:
                raise serializers.ValidationError("Invalid event type")
            return data
        except Exception as e:
            raise serializers.ValidationError(e)
