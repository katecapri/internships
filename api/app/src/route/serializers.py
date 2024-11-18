from rest_framework import serializers

from src.route.services.route_core import TemplateType, StepType, TimesheetDayType
from src.route.services.route_service import get_route_step_by_id, get_route_request_field_template_by_id
from src.user.services.user_service import get_group_by_code


def validate_template_type(template_type):
    is_template_type_valid = template_type in list(TemplateType)
    if not is_template_type_valid:
        raise serializers.ValidationError("Invalid template type")


def validate_group(group_code):
    group = get_group_by_code(group_code)
    if not group:
        raise serializers.ValidationError("Group with such code doesn`t exist")


def validate_groups(group_from_code, group_to_code):
    group_from = get_group_by_code(group_from_code)
    group_to = get_group_by_code(group_to_code)
    if not group_from or not group_to:
        raise serializers.ValidationError("One of groups doesn`t exist")
    if group_from.restricted_value != group_to.restricted_value:
        raise serializers.ValidationError("Groups don`t belong to the same role")


class TemplateRequestFieldTemplateSerializer(serializers.Serializer):
    fieldName = serializers.CharField()
    fieldType = serializers.CharField()
    mustBeVerified = serializers.BooleanField()
    correctnessCriteria = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    verificationValues = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    valuesForSelectField = serializers.CharField(allow_null=True, allow_blank=True, default=None)


class TemplateStepSerializer(serializers.Serializer):
    stepType = serializers.CharField()
    order = serializers.IntegerField()
    isStart = serializers.BooleanField()
    autoVerification = serializers.BooleanField()
    pointsValue = serializers.IntegerField()
    fields = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                   child=TemplateRequestFieldTemplateSerializer())
    timeSheetDuration = serializers.IntegerField(allow_null=True, default=None)
    timeSheetDurationItem = serializers.CharField(allow_null=True, default=None)
    minimumFillPercent = serializers.IntegerField(allow_null=True, default=None)

    def validate(self, data):
        try:
            if any([data["timeSheetDuration"], data["timeSheetDurationItem"], data["minimumFillPercent"]]):
                if data["stepType"] != StepType.timeSheet:
                    raise serializers.ValidationError("The timeSheet field is filled, but the step doesn`t have timeSheet type")
                if not data["timeSheetDuration"] and data["timeSheetDurationItem"] and data["minimumFillPercent"]:
                    raise serializers.ValidationError("All fields for the timeSheet must be completed")
                if data["fields"]:
                    raise serializers.ValidationError("A step cannot have a timeSheet field and a request field")
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class CreateTemplateSerializer(serializers.Serializer):
    templateType = serializers.CharField()
    fromGroup = serializers.CharField()
    toGroup = serializers.CharField()
    templateSteps = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                          child=TemplateStepSerializer())

    def validate(self, data):
        try:
            validate_template_type(data["templateType"])
            validate_groups(data["fromGroup"], data["toGroup"])
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class UpdateTemplateSerializer(serializers.Serializer):
    templateType = serializers.CharField(allow_null=True, default=None)
    fromGroup = serializers.CharField(allow_null=True, default=None)
    toGroup = serializers.CharField(allow_null=True, default=None)
    templateSteps = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                          child=TemplateStepSerializer())

    def validate(self, data):
        try:
            if data["templateType"]:
                validate_template_type(data["templateType"])
            if data["fromGroup"]:
                validate_group(data["fromGroup"])
            if data["toGroup"]:
                validate_group(data["toGroup"])
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class LaunchTemplateSerializer(serializers.Serializer):
    dateStart = serializers.CharField()
    dateEnd = serializers.CharField()


class RequestFieldSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    fieldValue = serializers.CharField()

    def validate_id(self, value):
        try:
            route_request_field_template = get_route_request_field_template_by_id(value)
            if not route_request_field_template:
                raise serializers.ValidationError("Route request field template with such id doesn`t exist")
            return value
        except Exception as e:
            raise serializers.ValidationError(e)


class CreateRequestSerializer(serializers.Serializer):
    routeId = serializers.UUIDField()
    routeStepId = serializers.UUIDField()
    fields = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                   child=RequestFieldSerializer())

    def validate(self, data):
        try:
            route_step = get_route_step_by_id(data["routeStepId"])
            if not route_step:
                raise serializers.ValidationError("Route step with such id doesn`t exist")
            if route_step.route_id != data["routeId"]:
                raise serializers.ValidationError("The route step doesn`t belong to the route")
            if route_step.step_type != StepType.request:
                raise serializers.ValidationError("The route step doesn`t have a request type")
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class SetTimesheetDaySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timeSheetDate = serializers.CharField()
    dayType = serializers.CharField()

    def validate_dayType(self, value):
        is_day_type_valid = value in list(TimesheetDayType)
        if is_day_type_valid:
            return value
        else:
            raise serializers.ValidationError("Invalid day type")
