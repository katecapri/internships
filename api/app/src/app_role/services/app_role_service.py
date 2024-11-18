import logging

from src.app_role.services.app_role_core import AppRolePermissionLevel, PermissionRuleData
from src.app_role.services.app_role_repository import AppRoleRepository


logger = logging.getLogger('app')


def get_permission_rules_by_app_role_id(app_role_id):
    db = AppRoleRepository()
    permission_rules = db.get_permission_rules_by_app_role_id(app_role_id)
    return permission_rules


def get_permission_rule(app_role_id, app_role_permission_id):
    db = AppRoleRepository()
    permission_rule = db.get_permission_rule(app_role_id, app_role_permission_id)
    return permission_rule


def get_app_role_permission_by_attrs(level: AppRolePermissionLevel, target_name_or_entry_point: str):
    db = AppRoleRepository()
    app_role_permission = db.get_app_role_permission_by_attrs(level, target_name_or_entry_point)
    return app_role_permission


def convert_app_role_object_to_representation(app_role):
    app_role_dict = {
        'id': app_role.id,
        'name': app_role.name,
        'code': app_role.code,
        'description': app_role.description
    }
    permissions = list()
    for permission in get_permission_rules_by_app_role_id(app_role.id):
        permission = permission[0]
        permission_dict = {
            'id': permission.app_role_permission.id,
            'level': permission.app_role_permission.level,
            'targetName': permission.app_role_permission.target_name,
            'entryPoint': permission.app_role_permission.entry_point,
            'hasAccess': permission.has_access,
            'createPermission': permission.create_permission,
            'readPermission': permission.read_permission,
            'updatePermission': permission.update_permission,
            'deletePermission': permission.delete_permission,
            'viewAllPermission': permission.view_all_permission,
            'modifyAllPermission': permission.modify_all_permission,
        }
        permissions.append(permission_dict)
    app_role_dict["permissions"] = permissions
    db = AppRoleRepository()
    groups_obj = db.get_groups_for_app_role_by_code(app_role.code)
    groups = list()
    for group in groups_obj:
        group_dict = {
                "id": group.id,
                "name": group.name,
                "code": group.code,
                "hierarchical": group.hierarchical,
                "parentGroupId": group.parent_group_id
            }
        groups.append(group_dict)
    app_role_dict["groups"] = groups
    return app_role_dict


def get_app_role_uuid_by_code(app_role_code: str):
    db = AppRoleRepository()
    app_role_uuid = db.get_app_role_uuid_by_code(app_role_code)
    return str(app_role_uuid)


def get_app_roles():
    db = AppRoleRepository()
    app_roles = db.get_app_roles()
    result = list()
    for app_role in app_roles:
        result.append(convert_app_role_object_to_representation(app_role[0]))
    return result


def get_app_role_by_id(app_role_id):
    db = AppRoleRepository()
    app_role = db.get_app_role_by_id(app_role_id)
    if app_role:
        return app_role
    else:
        return None


def check_app_role_permission_exists(app_role_permission_id):
    db = AppRoleRepository()
    app_role_permission = db.get_app_role_permission_by_id(app_role_permission_id)
    if app_role_permission:
        return True
    return False


def save_app_role_permission_rules(permission_rules, app_role_id):
    db = AppRoleRepository()
    for permission_rule in permission_rules:
        new_permission_rule = PermissionRuleData(
            app_role_id=app_role_id,
            app_role_permission_id=permission_rule["id"],
            has_access=permission_rule["hasAccess"],
            create_permission=permission_rule["createPermission"],
            read_permission=permission_rule["readPermission"],
            update_permission=permission_rule["updatePermission"],
            delete_permission=permission_rule["deletePermission"],
            view_all_permission=permission_rule["viewAllPermission"],
            modify_all_permission=permission_rule["modifyAllPermission"]
        )
        db.create_app_role_permission_rule(new_permission_rule)


def create_app_role(app_role_data):
    db = AppRoleRepository()
    existing_app_role_id = db.get_app_role_uuid_by_code(app_role_data["code"])
    if existing_app_role_id:
        logger.error("App role with such code already exists")
        return None
    new_app_role_id = db.create_app_role(app_role_data["name"], app_role_data["code"], app_role_data["description"])
    save_app_role_permission_rules(app_role_data["permissions"], new_app_role_id)
    result = get_app_role_by_id(new_app_role_id)
    return convert_app_role_object_to_representation(result)


def update_app_role(update_app_role_data, app_role_id):
    db = AppRoleRepository()
    existing_app_role_id = db.get_app_role_uuid_by_code(update_app_role_data["code"])
    if existing_app_role_id and existing_app_role_id != app_role_id:
        logger.error("App role with such code already exists")
        return None
    app_role = db.update_app_role(app_role_id, update_app_role_data["name"],
                                  update_app_role_data["code"], update_app_role_data["description"])
    if not app_role:
        return None
    db.delete_app_role_permission_rules_by_app_role_id(app_role_id)
    save_app_role_permission_rules(update_app_role_data["permissions"], app_role_id)
    result = get_app_role_by_id(app_role_id)
    return convert_app_role_object_to_representation(result)


def delete_app_role(app_role_id):
    db = AppRoleRepository()
    db.delete_app_role_by_id(app_role_id)
    return True
