import enum
from dataclasses import dataclass


class AppRolePermissionLevel(str, enum.Enum):
    COMPONENT = "COMPONENT"
    BUSINESS_OBJECT = "BUSINESS_OBJECT"


@dataclass
class PermissionRuleData:
    app_role_id: str
    app_role_permission_id: str
    has_access: bool
    create_permission: bool
    read_permission: bool
    update_permission: bool
    delete_permission: bool
    view_all_permission: bool
    modify_all_permission: bool
