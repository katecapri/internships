import logging
from enum import Enum

from src.app_role.models import AppRole, AppRolePermission, AppRolePermissionRule
from src.app_role.services.app_role_core import AppRolePermissionLevel
from src.app_role.services.app_role_service import get_app_role_permission_by_attrs, get_permission_rule


class EntryPoint(Enum):
    USER = "/user"
    APP_ROLE = "/appRole"
    DIRECTION = "/direction"
    PLACE = "/place"
    TEMPLATE = "/template"
    ROUTE = "/route"
    REQUEST = "/request"
    POINTS = "/points"


class PermissionType(Enum):
    CREATE = "create_permission"
    READ = "read_permission"
    UPDATE = "update_permission"
    DELETE = "delete_permission"
    VIEW_ALL = "view_all_permission"
    MODIFY_ALL = "modify_all_permission"


def get_object_property_by_permission_type(permission_type: PermissionType, permission_rule_obj: AppRolePermissionRule):
    if permission_type.value == "create_permission":
        return permission_rule_obj.create_permission
    elif permission_type.value == "read_permission":
        return permission_rule_obj.read_permission
    elif permission_type.value == "update_permission":
        return permission_rule_obj.update_permission
    elif permission_type.value == "delete_permission":
        return permission_rule_obj.delete_permission
    elif permission_type.value == "view_all_permission":
        return permission_rule_obj.view_all_permission
    elif permission_type.value == "modify_all_permission":
        return permission_rule_obj.modify_all_permission
    else:
        logging.error("Unknown permission type")


def has_user_permission(app_role: AppRole, permission_type: PermissionType, entry_point: EntryPoint) -> bool:
    app_role_permission = get_app_role_permission_by_attrs(AppRolePermissionLevel.BUSINESS_OBJECT, entry_point.value)
    permission_rule = get_permission_rule(app_role_id=app_role.id, app_role_permission_id=app_role_permission.id)
    result = get_object_property_by_permission_type(permission_type, permission_rule)
    return result
