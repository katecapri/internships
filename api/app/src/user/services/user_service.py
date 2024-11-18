import logging

from src.user.services.manager_service import send_reset_password_email
from src.user.services.user_core import CreateUserData, VerificationType
from src.user.services.user_repository import UserRepository
from src.user.services.verification_service import create_verification
from src.app_role.services.app_role_service import get_app_role_by_id, convert_app_role_object_to_representation, \
    get_app_role_uuid_by_code
from src.auth.services.password_service import encrypt_password
from src.route.services.timesheet_service import create_timesheet_for_new_trainee

logger = logging.getLogger('app')


def convert_user_to_representation(user):
    user_dict = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'isEmailConfirmed': user.is_email_confirmed
    }
    groups = list()
    for group in user.groups:
        group_dict = {
            "id": group.id,
            "name": group.name,
            "code": group.code,
            "hierarchical": group.hierarchical,
            "parentGroupId": group.parent_group_id
        }
        if group.code == 'traineeCandidate':
            candidate = get_candidate_by_user_id(user.id)
            if candidate:
                group_dict["isConfirmed"] = candidate.is_confirmed
            else:
                logger.error('The user is in a candidate group, but there is no information about the user in the candidates table')
                group_dict["isConfirmed"] = False
            if candidate.route_id:
                group_dict["routes"] = [
                    {
                        "id": candidate.route.id,
                        "routeType": candidate.route.route_type,
                        "dateStart": candidate.route.start_date,
                        "dateEnd": candidate.route.end_date,
                    }
                ]
        else:
            group_dict["isConfirmed"] = True
        if group.code == 'trainee':
            routes = list()
            for trainee in user.trainees:
                if trainee.route:
                    routes.append(
                        {
                            "id": trainee.route.id,
                            "routeType": trainee.route.route_type,
                            "dateStart": trainee.route.start_date,
                            "dateEnd": trainee.route.end_date,
                        }
                    )
            group_dict["routes"] = routes
        groups.append(group_dict)
    user_dict["groups"] = groups
    app_role = get_app_role_by_id(user.app_role_id)
    user_dict["appRole"] = convert_app_role_object_to_representation(app_role)
    return user_dict


def create_admin_user(new_admin_user: CreateUserData):
    db = UserRepository()
    if db.get_user_by_email(new_admin_user.email):
        return None
    new_user_uuid = db.create_user(new_admin_user)

    verification_code = create_verification(VerificationType.RESET_PASSWORD, new_user_uuid)
    send_reset_password_email(new_admin_user.email, verification_code)

    return new_admin_user


def get_user_by_id(user_id):
    db = UserRepository()
    return db.get_user_by_id(user_id)


def get_users():
    db = UserRepository()
    query_result = db.get_users()
    return query_result


def create_user(new_user_data: CreateUserData):
    db = UserRepository()
    new_user_uuid = db.create_user(new_user_data)
    if new_user_data.groups:
        candidate_group_id = get_group_by_code("traineeCandidate").id
        trainee_group_id = get_group_by_code("trainee").id
        for group in new_user_data.groups:
            db.save_user_group_relation(new_user_uuid, group["id"])
            if str(group["id"]) == str(candidate_group_id):
                db.save_new_candidate(new_user_uuid)
            if str(group["id"]) == str(trainee_group_id):
                db.save_new_trainee(new_user_uuid)
    return new_user_uuid


def update_user(user_id, update_user_info):
    db = UserRepository()
    if update_user_info["password"]:
        encrypted_password = encrypt_password(update_user_info["password"])
        encrypted_password = encrypted_password.decode()
        db.update_user_password(user_id, encrypted_password)
        update_user_info.pop('password', None)
    if any([update_user_info["email"], update_user_info["name"],
            update_user_info["isEmailConfirmed"], update_user_info["appRoleId"]]):
        db.update_user(user_id, update_user_info)
    if update_user_info["groups"] is not None:
        db.delete_user_groups_by_user_id(user_id)
        if len(update_user_info["groups"]) > 0:
            candidate_group_id = get_group_by_code("traineeCandidate").id
            trainee_group_id = get_group_by_code("trainee").id
            for group in update_user_info["groups"]:
                db.save_user_group_relation(user_id, group["id"])
                if str(group["id"]) == str(candidate_group_id):
                    if get_candidate_by_user_id(user_id):
                        logger.error('Candidate not added, user already has a row in the candidates table')
                    else:
                        db.save_new_candidate(user_id)
                if str(group["id"]) == str(trainee_group_id):
                    trainee = get_trainee_by_user_id(user_id)
                    if trainee:
                        logger.error('Trainee not added, user already has a row in the trainees table')
                    else:
                        db.save_new_trainee(user_id)
                    route = group["routes"][0]
                    db.set_route_to_trainee(user_id, route["id"])
                    create_timesheet_for_new_trainee(user_id, trainee.route)
    return user_id


def delete_user(user_id):
    db = UserRepository()
    db.delete_user(user_id)


def check_app_role_belongs_to_user(app_role_id):
    db = UserRepository()
    users = db.get_users_by_app_role_id(app_role_id)
    if users:
        return True
    else:
        return False


def get_user_by_email(user_email):
    db = UserRepository()
    return db.get_user_by_email(user_email)


def check_user_can_use_method(request, user_id):
    if not hasattr(request, "hackathonUser"):
        logger.error('User must be authorized for this method')
        return False
    if user_id != request.hackathonUser.id:
        user_app_role = get_app_role_by_id(request.hackathonUser.app_role_id)
        if user_app_role.code not in ["ADMIN", "MANAGER"]:
            logger.error('User app role doesn`t allow changing information about other users')
            return False
    return True


def check_user_manager_or_admin(request):
    if not hasattr(request, "hackathonUser"):
        logger.error('User must be authorized for this method')
        return False
    user_app_role = get_app_role_by_id(request.hackathonUser.app_role_id)
    if user_app_role.code not in ["ADMIN", "MANAGER"]:
        logger.error('User app role doesn`t allow using this method')
        return False
    return True


def get_group_by_id(group_id):
    db = UserRepository()
    return db.get_group_by_id(group_id)


def get_groups_by_restricted_value_for_app_role(restricted_value):
    db = UserRepository()
    return db.get_groups_by_restricted_value_for_app_role(restricted_value)


def get_group_by_name(group_name):
    db = UserRepository()
    return db.get_group_by_name(group_name)


def get_group_by_code(group_code):
    db = UserRepository()
    return db.get_group_by_code(group_code)


def check_new_role_and_groups_are_valid(user, data_to_update_user, available_groups_for_roles):
    new_app_role_id = data_to_update_user["appRoleId"]
    current_app_role_id = user.app_role_id
    if new_app_role_id is None:
        if data_to_update_user["groups"] is None:
            return True
        elif len(data_to_update_user["groups"]) == 0:
            if user.app_role_id in available_groups_for_roles.keys():
                logger.error('Old app role + 0 new groups: '
                             'Deleting user groups forbidden if there are assigned groups for app role.')
                return False
            else:
                return True
        else:
            for group in data_to_update_user["groups"]:
                group_obj = get_group_by_id(group["id"])
                if group_obj.restricted == "APP_ROLE":
                    if group_obj.restricted_value != get_app_role_by_id(current_app_role_id).code:
                        logger.error("Old app role + any new groups: "
                                     "The new group doesn`t match the current user app role.")
                        return False
            return True
    else:
        if data_to_update_user["groups"] is None:
            if user.groups:
                for group in user.groups:
                    if group.restricted == "APP_ROLE":
                        logger.error("New app role + old groups: "
                                     "The new user app role doesn`t match non-updatable old groups.")
                        return False
            if new_app_role_id not in available_groups_for_roles.keys():
                return True
            else:
                logger.error("New app role + old groups: "
                             "A group must be selected for the new app role.")
                return False
        elif len(data_to_update_user["groups"]) == 0:
            if new_app_role_id in available_groups_for_roles.keys():
                logger.error('New app role + 0 new groups: '
                             'Deleting user groups forbidden if there are assigned groups for new app role.')
                return False
            else:
                return True
        else:
            for group in data_to_update_user["groups"]:
                group_obj = get_group_by_id(group["id"])
                if group_obj.restricted == "APP_ROLE":
                    if group_obj.restricted_value != get_app_role_by_id(new_app_role_id).code:
                        logger.error("New app role + any new groups: "
                                     "The new group doesn`t match the new app role.")
                        return False
            return True


def get_candidate_by_user_id(user_id):
    db = UserRepository()
    return db.get_candidate_by_user_id(user_id)


def get_trainee_by_user_id(user_id):
    db = UserRepository()
    return db.get_trainee_by_user_id(user_id)


def confirm_candidate(user_id):
    db = UserRepository()
    return db.confirm_candidate(user_id)


def get_trainees_by_route_id(route_id):
    db = UserRepository()
    query_result = db.get_trainees_by_route_id(route_id)
    result = [trainee[0] for trainee in query_result]
    return result


def set_route_to_candidate(user_id, route_id):
    db = UserRepository()
    db.set_route_to_candidate(user_id, route_id)

