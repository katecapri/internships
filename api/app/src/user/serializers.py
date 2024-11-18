from rest_framework import serializers
from src.app_role.services.app_role_service import get_app_role_uuid_by_code, get_app_role_by_id
from src.route.services.route_core import RouteType
from src.route.services.route_service import get_route_by_id
from src.user.services.user_service import get_user_by_email, get_group_by_id, \
    get_groups_by_restricted_value_for_app_role, get_group_by_name

available_groups_for_roles = {
    get_app_role_uuid_by_code("APP_USER"): {
        'groups': [get_groups_by_restricted_value_for_app_role("APP_USER")],
        'default_group_id': get_group_by_name('Кандидат').id
    },
    get_app_role_uuid_by_code("MANAGER"): {
        'groups': [get_groups_by_restricted_value_for_app_role("MANAGER")],
    },
}


def validate_email(email):
    user = get_user_by_email(email)
    if user:
        raise serializers.ValidationError("User with such email already exists")


class RouteSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, value):
        try:
            if get_route_by_id(value):
                return value
            raise serializers.ValidationError("Route with such id does not exist")
        except Exception as e:
            raise serializers.ValidationError(e)


class UpdateUserGroupSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    routes = serializers.ListField(allow_null=True, default=None, allow_empty=True, child=RouteSerializer())

    def validate(self, data):
        try:
            group = get_group_by_id(data["id"])
            if not group:
                raise serializers.ValidationError("Group with such id does not exist")
            if group.code == "trainee":
                if not data["routes"]:
                    raise serializers.ValidationError("The trainee must be assigned a route")
                for route in data["routes"]:
                    if get_route_by_id(route["id"]).route_type != RouteType.internship:
                        raise serializers.ValidationError("The trainee must be assigned a route with internship type")
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class CreateUserGroupSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, value):
        try:
            if get_group_by_id(value):
                return value
            raise serializers.ValidationError("Group with such id does not exist")
        except Exception as e:
            raise serializers.ValidationError(e)


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    appRoleId = serializers.CharField(allow_null=True, allow_blank=True, default=get_app_role_uuid_by_code("APP_USER"))
    groups = serializers.ListField(allow_null=True, default=None, allow_empty=True, child=CreateUserGroupSerializer())

    def validate(self, data):
        try:
            global available_groups_for_roles
            validate_email(data["email"])
            if data["groups"] is None or (data["groups"] is not None and len(data["groups"]) == 0):
                if data["appRoleId"] not in available_groups_for_roles.keys():
                    return data
                else:
                    if "default_group_id" in available_groups_for_roles[data["appRoleId"]]:
                        data["groups"] = [{"id": available_groups_for_roles[data["appRoleId"]]["default_group_id"]}]
                    else:
                        raise serializers.ValidationError("For this role, the group must be filled")
            else:
                for group in data["groups"]:
                    group_obj = get_group_by_id(group["id"])
                    if group_obj.restricted == "APP_ROLE":
                        if group_obj.restricted_value != get_app_role_by_id(data["appRoleId"]).code:
                            raise serializers.ValidationError("The group doesn`t match the app role")
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class UpdateUserSerializer(serializers.Serializer):
    email = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    password = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    name = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    isEmailConfirmed = serializers.BooleanField(allow_null=True, default=None)
    appRoleId = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    groups = serializers.ListField(allow_null=True, default=None, allow_empty=True, child=UpdateUserGroupSerializer())

    def validate(self, data):
        try:
            if data["email"]:
                validate_email(data["email"])
            if not any([data["email"], data["name"], data["password"], data["isEmailConfirmed"],
                        data["appRoleId"], data["groups"] is not None]):
                raise serializers.ValidationError('One of the fields must be filled')
            return data
        except Exception as e:
            raise serializers.ValidationError(e)
