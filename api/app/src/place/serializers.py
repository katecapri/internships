from rest_framework import serializers
from src.place.services.place_service import get_direction_by_name, check_department_exists, get_place_by_name


def validate_name(name_type, value):
    try:
        if value:
            if name_type == "direction":
                direction = get_direction_by_name(value)
                if direction:
                    raise serializers.ValidationError("Direction with such name already exists")
            if name_type == "place":
                place = get_place_by_name(value)
                if place:
                    raise serializers.ValidationError("Place with such name already exists")
        return value
    except Exception as e:
        raise serializers.ValidationError(e)


class DepartmentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(allow_null=True, default=None)

    def validate_id(self, value):
        try:
            if check_department_exists(value):
                return value
            raise serializers.ValidationError("Department with such id does not exist")
        except Exception as e:
            raise serializers.ValidationError(e)


class UpdateDirectionSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, default=None)
    display = serializers.CharField(allow_null=True, default=None)
    departments = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                        child=DepartmentSerializer())

    def validate_name(self, value):
        return validate_name("direction", value)


class UpdatePlaceSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, default=None)
    address = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    departments = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                        child=DepartmentSerializer())

    def validate_name(self, value):
        return validate_name("place", value)


class CreatePlaceSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    departments = serializers.ListField(allow_null=True, default=None, allow_empty=True,
                                        child=DepartmentSerializer())

    def validate_name(self, value):
        return validate_name("place", value)
