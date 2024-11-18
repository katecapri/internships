import logging
import json
from math import ceil

from src.route.services.route_repository import RouteRepository
from src.route.services.route_core import RouteDateStatus, CorrectnessCriteria, RequestStatus, StepType
from src.user.services.user_service import get_group_by_code, get_candidate_by_user_id, \
    confirm_candidate, set_route_to_candidate
from src.points.services.points_core import EventType, PointsEventData
from src.points.services.points_service import prepare_points_event_info_for_queue

from src.message_broker.producer import send_into_request_verify_queue

logger = logging.getLogger('app')


def convert_steps_and_request_field_templates_for_representation(steps_obj):
    steps = list()
    for step in steps_obj:
        step_dict = {
            'id': step.id,
            'stepType': step.step_type,
            'order': step.order,
            'isStart': step.is_start,
            'autoVerification': step.auto_verification,
            'pointsValue': step.points_value
        }
        if step.step_type == StepType.request:
            fields = list()
            for request_field_template in step.request_field_templates:
                field_dict = {
                    'id': request_field_template.id,
                    'fieldName': request_field_template.field_name,
                    'fieldType': request_field_template.field_type,
                    'valuesForSelectField': request_field_template.values_for_select_field,
                    'mustBeVerified': request_field_template.must_be_verified,
                    'correctnessCriteria': request_field_template.correctness_criteria,
                    'verificationValues': request_field_template.verification_value,
                }
                fields.append(field_dict)
            step_dict["fields"] = fields
        else:
            if step.time_sheep_step:
                step_dict["duration"] = step.time_sheep_step[0].duration
                step_dict["durationItem"] = step.time_sheep_step[0].duration_item
                step_dict["minimumFillPercent"] = step.time_sheep_step[0].minimum_fill_percent
        steps.append(step_dict)
    return steps


def convert_template_to_representation(template):
    template_dict = {
        'id': template.id,
        'templateType': template.template_type,
        'fromGroup': template.from_group,
        'toGroup': template.to_group
    }
    template_steps = convert_steps_and_request_field_templates_for_representation(template.steps)
    template_dict["templateSteps"] = template_steps
    return template_dict


def convert_route_to_representation(route):
    route_dict = {
        'id': route.id,
        'routeType': route.route_type,
        'fromGroup': route.from_group,
        'toGroup': route.to_group,
        'dateStart': route.start_date,
        'dateEnd': route.end_date
    }
    route_steps = convert_steps_and_request_field_templates_for_representation(route.steps)
    route_dict["routeSteps"] = route_steps
    return route_dict


def convert_request_for_user(request):
    request_dict = {
        "id": request.id,
        "requestStatus": request.request_status,
        "dateCreated": str(request.creation_date),
        "dateApproved": str(request.approval_date),
        "dateRejected": str(request.rejection_date),
        "routeId": request.route_step.route_id,
        "routeStepId": request.route_step_id,
    }
    return request_dict


def convert_request_for_route(request):
    request_dict = {
        "id": request.id,
        "requestStatus": request.request_status,
        "dateCreated": str(request.creation_date),
        "routeId": request.route_step.route_id,
        "routeStepId": request.route_step_id,
        "userName": request.user.name,
        "userEmail": request.user.email,
        "fields": [
            {
                "id": field.id,
                "fieldName": field.field_name,
                "fieldValue": field.field_value,
                "isVerified": is_request_field_verified(field)
            } for field in request.fields
        ]
    }
    return request_dict


def is_request_field_verified(request_field):
    if request_field.correctness_criteria == CorrectnessCriteria.quality:
        if request_field.field_value != request_field.verification_value:
            return False
    elif request_field.correctness_criteria == CorrectnessCriteria.range:
        if float(request_field.field_value) <= float(json.loads(request_field.verification_value)["min"]) \
                or float(json.loads(request_field.verification_value)["max"]) <= float(request_field.field_value):
            return False
    return True


def get_templates():
    db = RouteRepository()
    query_result = db.get_templates()
    result = [template[0] for template in query_result]
    return result


def get_template_by_id(template_id):
    db = RouteRepository()
    return db.get_template_by_id(template_id)


def update_template(template_id, update_template_data):
    db = RouteRepository()
    if any([update_template_data["templateType"], update_template_data["fromGroup"], update_template_data["toGroup"]]):
        template = db.update_template(template_id, update_template_data)
        if not template:
            return None
    if update_template_data["templateSteps"] is None:
        return template_id
    db.delete_template_steps_by_template_id(template_id)
    if len(update_template_data["templateSteps"]) == 0:
        return template_id
    for step in update_template_data["templateSteps"]:
        new_step_id = db.save_template_step(template_id, step)
        if step["stepType"] == StepType.request:
            if step["fields"] is not None and len(step["fields"]) > 0:
                for field in step["fields"]:
                    db.save_template_field(new_step_id, field)
        else:
            if any([step["timeSheetDuration"], step["timeSheetDurationItem"], step["minimumFillPercent"]]):
                db.save_template_time_sheet(new_step_id, step)
    return template_id


def create_template(template_data):
    db = RouteRepository()
    new_template_id = db.create_template(template_data)
    if template_data["templateSteps"] is None or len(template_data["templateSteps"]) == 0:
        return get_template_by_id(new_template_id)
    for step in template_data["templateSteps"]:
        new_step_id = db.save_template_step(new_template_id, step)
        if step["stepType"] == StepType.request:
            if step["fields"] is not None and len(step["fields"]) > 0:
                for field in step["fields"]:
                    db.save_template_field(new_step_id, field)
        else:
            if any([step["timeSheetDuration"], step["timeSheetDurationItem"], step["minimumFillPercent"]]):
                db.save_template_time_sheet(new_step_id, step)
    return get_template_by_id(new_template_id)


def check_groups_correct_after_updating(current_template_obj, update_data):
    group_from_code = update_data["fromGroup"] if update_data["fromGroup"] else current_template_obj.from_group
    group_to_code = update_data["toGroup"] if update_data["toGroup"] else current_template_obj.to_group
    group_from = get_group_by_code(group_from_code)
    group_to = get_group_by_code(group_to_code)
    return True if group_from.restricted_value == group_to.restricted_value else False


def get_route_by_id(route_id):
    db = RouteRepository()
    return db.get_route_by_id(route_id)


def launch_template(template_obj, launch_data):
    db = RouteRepository()
    new_route_id = db.launch_template(template_obj, launch_data)
    if not template_obj.steps:
        return get_route_by_id(new_route_id)
    for template_step in template_obj.steps:
        new_step_id = db.save_route_step(new_route_id, template_step)
        if template_step.request_field_templates:
            for field in template_step.request_field_templates:
                db.save_route_field(new_step_id, field)
        if template_step.time_sheep_step:
            db.save_route_time_sheet(new_step_id, template_step.time_sheep_step[0])
    return get_route_by_id(new_route_id)


def get_routes(user):
    db = RouteRepository()
    if user.app_role.code != "APP_USER":
        query_result = db.get_all_routes()
        result = [route[0] for route in query_result]
        return result
    user_groups = [group.code for group in user.groups]
    result = list()
    if 'traineeCandidate' in user_groups:
        user_candidate = get_candidate_by_user_id(user.id)
        if user_candidate:
            routes_id = list()
            if user_candidate.is_confirmed:
                candidate_routes = db.get_routes_by_date_status_and_from_group_code(
                    RouteDateStatus.active, 'traineeCandidate')
            else:
                candidate_routes = db.get_routes_by_date_status_and_from_group_code(
                    RouteDateStatus.planned, 'traineeCandidate')
            for route in candidate_routes:
                result.append(route[0])
                routes_id.append(route[0].id)
            if user_candidate.route_id and user_candidate.route_id not in routes_id:
                result.append(get_route_by_id(user_candidate.route_id))
        else:
            logger.error("User has a candidate group, but doesn`t have a row in candidates table")
    if 'trainee' in user_groups:
        trainee_routes = db.get_routes_by_date_status_and_from_group_code(RouteDateStatus.active, 'trainee')
        result.extend([route[0] for route in trainee_routes])
    if 'graduate' in user_groups:
        graduate_routes = db.get_routes_by_date_status_and_from_group_code(RouteDateStatus.no_matter, 'graduate')
        result.extend([route[0] for route in graduate_routes])
    return result


def get_page_of_requests(offset, limit, user_id=None):
    db = RouteRepository()
    all_requests = db.get_requests_by_user_id(user_id)
    count = len(all_requests)
    max_page = ceil(count / limit)
    has_more = True if offset < max_page else False
    result = {
        "count": count,
        "page": offset,
        "hasMore": has_more,
        "pagesMax": max_page
    }
    if count == 0:
        items = []
    else:
        start_item = (offset - 1) * limit + 1
        if has_more:
            end_item = start_item + limit - 1
        else:
            end_item = count
        requests_for_page = all_requests[start_item - 1:end_item]
        items = [convert_request_for_user(request[0]) for request in requests_for_page]
    result["items"] = items
    return result


def get_requests_by_route_step_id(route_step_id):
    db = RouteRepository()
    query_result = db.get_requests_by_route_step_id(route_step_id)
    result = [request[0] for request in query_result]
    return result


def create_request(request_data, user_id):
    db = RouteRepository()
    new_request_id = db.create_request(request_data, user_id)
    set_route_to_candidate(user_id, request_data["routeId"])
    if request_data["fields"] is None or len(request_data["fields"]) == 0:
        return check_auto_verify_to_new_request(new_request_id)
    for field in request_data["fields"]:
        route_request_field_template = db.get_route_request_field_template_by_id(field["id"])
        db.save_request_field(new_request_id, field["fieldValue"], route_request_field_template)
    return check_auto_verify_to_new_request(new_request_id)


def get_route_step_by_id(route_step_id):
    db = RouteRepository()
    return db.get_route_step_by_id(route_step_id)


def get_request_verification_by_request_id(request_id):
    db = RouteRepository()
    return db.get_request_verification_by_request_id(request_id)


def check_auto_verify_to_new_request(request_id):
    db = RouteRepository()
    request = db.get_request_by_id(request_id)
    if request.route_step.auto_verification:
        send_into_request_verify_queue(str(request_id))
    return request_id


def get_error_for_request_field(field):
    error = {
        'fieldName': field.field_name,
        'correctnessCriteria': field.correctness_criteria,
        'verificationValue': field.verification_value,
        'fieldValue': field.field_value,
    }
    return error


def verify_request(request_id):
    db = RouteRepository()
    request = db.get_request_by_id(request_id)
    for field in request.fields:
        if field.must_be_verified:
            if field.correctness_criteria == CorrectnessCriteria.quality:
                if field.field_value != field.verification_value:
                    error = get_error_for_request_field(field)
                    db.save_request_verification(request_id, json.dumps(error))
                    db.change_request_status(request_id, RequestStatus.rejected)
                    return
            elif field.correctness_criteria == CorrectnessCriteria.range:
                if float(field.field_value) <= float(json.loads(field.verification_value)["min"]) \
                        or float(json.loads(field.verification_value)["max"]) <= float(field.field_value):
                    error = get_error_for_request_field(field)
                    db.save_request_verification(request_id, json.dumps(error))
                    db.change_request_status(request_id, RequestStatus.rejected)
                    return
    db.save_request_verification(request_id)
    db.change_request_status(request_id, RequestStatus.approved)
    confirm_candidate(request.user_id)
    if float(request.route_step.points_value) > 0:
        points_increase_info = PointsEventData(
            user_id=request.user_id, event_type=EventType.INCREASE,
            points_value=request.route_step.points_value, reason='Request approval'
        )
        prepare_points_event_info_for_queue(points_increase_info)


def get_route_request_field_template_by_id(route_request_field_template_id):
    db = RouteRepository()
    return db.get_route_request_field_template_by_id(route_request_field_template_id)
