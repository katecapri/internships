from rest_framework import serializers

from src.app_role.services.app_role_service import check_app_role_permission_exists


class AppRolePermissionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    level = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    targetName = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    entryPoint = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    hasAccess = serializers.BooleanField()
    createPermission = serializers.BooleanField()
    readPermission = serializers.BooleanField()
    updatePermission = serializers.BooleanField()
    deletePermission = serializers.BooleanField()
    viewAllPermission = serializers.BooleanField()
    modifyAllPermission = serializers.BooleanField()

    def validate_id(self, value):
        try:
            if check_app_role_permission_exists(value):
                return value
            raise serializers.ValidationError("App role permission with such id does not exist")
        except Exception as e:
            raise serializers.ValidationError(e)


class AppRoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    permissions = serializers.ListField(allow_null=True, default=[], allow_empty=True,
                                        child=AppRolePermissionSerializer())
