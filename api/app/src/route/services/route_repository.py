from uuid import uuid4
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from src.route.models import Template, TemplateStep, TemplateRequestFieldTemplate, \
    Route, RouteStep, RouteRequestFieldTemplate, Request, RequestField, RequestVerification, \
    TemplateTimeSheepStep, RouteTimeSheepStep
from src.route.services.route_core import RouteDateStatus, RequestStatus
from src.base_crud import BaseCRUD
from src.init_database import Session


class RouteRepository:
    def __init__(self):
        self.db_session = Session
        self.model_template = Template
        self.model_template_step = TemplateStep
        self.model_template_request_field_template = TemplateRequestFieldTemplate
        self.model_route = Route
        self.model_route_step = RouteStep
        self.model_route_request_field_template = RouteRequestFieldTemplate
        self.model_request = Request
        self.model_request_field = RequestField
        self.model_request_verification = RequestVerification
        self.model_template_time_sheet_step = TemplateTimeSheepStep
        self.model_route_time_sheet_step = RouteTimeSheepStep
        self.base = BaseCRUD(db_session=self.db_session)

    def get_templates(self):
        try:
            with self.base.transaction():
                stmt = select(self.model_template)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_template_by_id(self, template_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_template) \
                    .where(self.model_template.id == template_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_all_routes(self):
        try:
            with self.base.transaction():
                stmt = select(self.model_route)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_route_by_id(self, route_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_route) \
                    .where(self.model_route.id == route_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_route_step_by_id(self, route_step_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_route_step) \
                    .where(self.model_route_step.id == route_step_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_routes_by_date_status_and_from_group_code(self, date_status, from_group_code):
        try:
            with self.base.transaction():
                stmt = select(self.model_route) \
                    .where(self.model_route.from_group == from_group_code)
                if date_status == RouteDateStatus.active:
                    stmt = stmt.where(self.model_route.start_date < datetime.now(),
                                      datetime.now() < self.model_route.end_date)
                if date_status == RouteDateStatus.planned:
                    stmt = stmt.where(datetime.now() < self.model_route.start_date)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def create_template(self, template_data):
        with self.base.transaction():
            new_template_id = uuid4()
            self.base.insert(
                self.model_template,
                id=new_template_id,
                template_type=template_data["templateType"],
                from_group=template_data["fromGroup"],
                to_group=template_data["toGroup"],
                creation_date=datetime.now(),
            )
            self.base.commit()
        return new_template_id

    def update_template(self, template_id, update_template_data):
        try:
            stmt = update(self.model_template).where(
                self.model_template.id == template_id,
            )
            if update_template_data["templateType"]:
                stmt = stmt.values(template_type=update_template_data["templateType"])
            if update_template_data["fromGroup"]:
                stmt = stmt.values(from_group=update_template_data["fromGroup"])
            if update_template_data["toGroup"]:
                stmt = stmt.values(to_group=update_template_data["toGroup"])
            stmt = stmt.returning(self.model_template)
            return self.base.update_by_statement(self.model_template, stmt)
        except NoResultFound:
            return None

    def delete_template_steps_by_template_id(self, template_id):
        try:
            stmt = delete(self.model_template_step)\
                .where(self.model_template_step.template_id == template_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def save_template_step(self, template_id, step_data):
        with self.base.transaction():
            new_template_step_id = uuid4()
            self.base.insert(
                self.model_template_step,
                id=new_template_step_id,
                step_type=step_data["stepType"],
                order=step_data["order"],
                is_start=step_data["isStart"],
                auto_verification=step_data["autoVerification"],
                points_value=step_data["pointsValue"],
                template_id=template_id,
            )
            self.base.commit()
        return new_template_step_id

    def save_template_field(self, step_id, field_data):
        with self.base.transaction():
            new_field_id = uuid4()
            self.base.insert(
                self.model_template_request_field_template,
                id=new_field_id,
                field_name=field_data["fieldName"],
                field_type=field_data["fieldType"],
                values_for_select_field=field_data["valuesForSelectField"],
                must_be_verified=field_data["mustBeVerified"],
                correctness_criteria=field_data["correctnessCriteria"],
                verification_value=field_data["verificationValues"],
                template_step_id=step_id,
            )
            self.base.commit()
        return new_field_id

    def save_template_time_sheet(self, step_id, step_data):
        with self.base.transaction():
            new_template_time_sheet_id = uuid4()
            self.base.insert(
                self.model_template_time_sheet_step,
                id=new_template_time_sheet_id,
                template_step_id=step_id,
                duration=step_data["timeSheetDuration"],
                duration_item=step_data["timeSheetDurationItem"],
                minimum_fill_percent=step_data["minimumFillPercent"],
            )
            self.base.commit()
        return new_template_time_sheet_id

    def launch_template(self, template_obj, launch_data):
        with self.base.transaction():
            new_route_id = uuid4()
            self.base.insert(
                self.model_route,
                id=new_route_id,
                route_type=template_obj.template_type,
                from_group=template_obj.from_group,
                to_group=template_obj.to_group,
                creation_date=datetime.now(),
                start_date=datetime.strptime(launch_data["dateStart"], '%Y-%m-%d'),
                end_date=datetime.strptime(launch_data["dateEnd"], '%Y-%m-%d'),
            )
            self.base.commit()
        return new_route_id

    def save_route_step(self, route_id, template_step):
        with self.base.transaction():
            new_route_step_id = uuid4()
            self.base.insert(
                self.model_route_step,
                id=new_route_step_id,
                step_type=template_step.step_type,
                order=template_step.order,
                is_start=template_step.is_start,
                auto_verification=template_step.auto_verification,
                points_value=template_step.points_value,
                route_id=route_id,
            )
            self.base.commit()
        return new_route_step_id

    def save_route_field(self, route_step_id, template_field):
        with self.base.transaction():
            new_field_id = uuid4()
            self.base.insert(
                self.model_route_request_field_template,
                id=new_field_id,
                field_name=template_field.field_name,
                field_type=template_field.field_type,
                values_for_select_field=template_field.values_for_select_field,
                must_be_verified=template_field.must_be_verified,
                correctness_criteria=template_field.correctness_criteria,
                verification_value=template_field.verification_value,
                route_step_id=route_step_id,
            )
            self.base.commit()
        return new_field_id

    def save_route_time_sheet(self, step_id, template_time_sheet_step):
        with self.base.transaction():
            new_route_time_sheet_id = uuid4()
            self.base.insert(
                self.model_route_time_sheet_step,
                id=new_route_time_sheet_id,
                route_step_id=step_id,
                duration=template_time_sheet_step.duration,
                duration_item=template_time_sheet_step.duration_item,
                minimum_fill_percent=template_time_sheet_step.minimum_fill_percent,
            )
            self.base.commit()
        return new_route_time_sheet_id

    def get_requests_by_user_id(self, user_id=None):
        try:
            with self.base.transaction():
                stmt = select(self.model_request)
                if user_id:
                    stmt = stmt.where(self.model_request.user_id == user_id)
                stmt = stmt.order_by(self.model_request.creation_date.desc())
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_request_by_id(self, request_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_request).where(self.model_request.id == request_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_requests_by_route_step_id(self, route_step_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_request).where(self.model_request.route_step_id == route_step_id)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_request_verification_by_request_id(self, request_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_request_verification) \
                    .where(self.model_request_verification.request_id == request_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def create_request(self, request_data, user_id):
        with self.base.transaction():
            new_request_id = uuid4()
            self.base.insert(
                self.model_request,
                id=new_request_id,
                user_id=user_id,
                request_status=RequestStatus.underConsideration,
                route_step_id=request_data["routeStepId"],
                creation_date=datetime.now(),
            )
            self.base.commit()
        return new_request_id

    def save_request_field(self, request_id, field_value, route_request_field_template):
        with self.base.transaction():
            new_field_id = uuid4()
            self.base.insert(
                self.model_request_field,
                id=new_field_id,
                field_name=route_request_field_template.field_name,
                field_type=route_request_field_template.field_type,
                field_value=field_value,
                values_for_select_field=route_request_field_template.values_for_select_field,
                must_be_verified=route_request_field_template.must_be_verified,
                correctness_criteria=route_request_field_template.correctness_criteria,
                verification_value=route_request_field_template.verification_value,
                request_id=request_id,
            )
            self.base.commit()
        return new_field_id

    def save_request_verification(self, request_id, error=None):
        with self.base.transaction():
            new_verification_id = uuid4()
            self.base.insert(
                self.model_request_verification,
                id=new_verification_id,
                request_id=request_id,
                creation_date=datetime.now(),
                is_correct=not bool(error),
                verification_error=error,
            )
            self.base.commit()
        return new_verification_id

    def get_route_request_field_template_by_id(self, route_request_field_template_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_route_request_field_template)\
                    .where(self.model_route_request_field_template.id == route_request_field_template_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def change_request_status(self, request_id, request_status: RequestStatus):
        try:
            stmt = update(self.model_request).where(
                self.model_request.id == request_id,
            ).values(request_status=request_status)
            if request_status == RequestStatus.approved:
                stmt = stmt.values(approval_date=datetime.now())
            else:
                stmt = stmt.values(rejection_date=datetime.now())
            stmt = stmt.returning(self.model_request)
            return self.base.update_by_statement(self.model_request, stmt)
        except NoResultFound:
            return None
