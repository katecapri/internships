import json
from datetime import datetime, timedelta

from src.timesheet.services.timesheet_core import EventType, DurationItem
from src.timesheet.services.timesheet_repository import TimesheetRepository


def get_timesheet_days_by_user_and_route(user_id, route_id):
    db = TimesheetRepository()
    timesheet_days = db.get_timesheet_days_by_user_and_route(user_id, route_id)
    if not timesheet_days:
        return []
    result = [
        {
            "id": timesheet_day[0].id,
            "timeSheetDate": timesheet_day[0].timesheet_date,
            "dayType": timesheet_day[0].date_type,
        } for timesheet_day in timesheet_days
    ]
    return result


def get_timesheet_event_by_id(event_id):
    db = TimesheetRepository()
    return db.get_timesheet_event_by_id(event_id)


def generate_or_update_timesheet(timesheet_info):
    event_id = timesheet_info["eventId"]
    user_id = timesheet_info["userId"]
    route_id = timesheet_info["routeId"]
    db = TimesheetRepository()
    db.create_timesheet_event(event_id, user_id, route_id, json.dumps(timesheet_info))
    if timesheet_info["eventType"] == EventType.generate:
        not_interrupted = generate_timesheet(user_id, route_id, timesheet_info["toGenerate"])
    else:
        not_interrupted = update_timesheet(user_id, route_id, timesheet_info["toUpdate"])
    close_timesheet_event(event_id, not not_interrupted)
    return not_interrupted


def generate_timesheet(user_id, route_id, generate_info):
    start_date_str = generate_info["dateStart"]
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    if generate_info["durationItem"] == DurationItem.days:
        duration = timedelta(days=generate_info["duration"] - 1)
    elif generate_info["durationItem"] == DurationItem.months:
        duration = timedelta(days=30 * generate_info["duration"] - 1)
    else:
        return None
    end_date = start_date + duration
    db = TimesheetRepository()
    not_interrupted = db.create_new_timesheet(user_id, route_id, start_date, end_date)
    return not_interrupted


def update_timesheet(user_id, route_id, update_info):
    db = TimesheetRepository()
    not_interrupted = db.update_timesheet_day(user_id, route_id, update_info["eventDate"], update_info["dayType"])
    return not_interrupted


def close_timesheet_event(event_id, is_interrupted):
    db = TimesheetRepository()
    db.close_timesheet_event(event_id, is_interrupted)
