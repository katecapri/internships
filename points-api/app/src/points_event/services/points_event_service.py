from math import ceil

from src.points_event.services.points_event_core import EventType, PointsEventData
from src.points_event.services.points_event_repository import PointsEventRepository


def get_points_events_for_user(user_id, offset, limit):
    db = PointsEventRepository()
    all_points_events = db.get_points_events_by_user_id(user_id)
    count = len(all_points_events)
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
        points_events_for_page = all_points_events[start_item - 1:end_item]
        items = [
            {
                "userId": points_event[0].owner_id,
                "eventType": "increase" if points_event[0].increase else "decrease",
                "pointsValue": points_event[0].value,
                "dateCreated": points_event[0].creation_date,
                "reason": points_event[0].reason,
            } for points_event in points_events_for_page
        ]
    result["items"] = items
    return result


def create_points_event(create_points_event_data):
    db = PointsEventRepository()
    new_points_event_data = PointsEventData(
        id=create_points_event_data["id"],
        owner_id=create_points_event_data["ownerId"],
        increase=True if create_points_event_data["eventType"] == EventType.INCREASE else False,
        value=create_points_event_data["pointsValue"],
        reason=create_points_event_data["reason"]
    )
    new_points_event_id = db.save_points_event(new_points_event_data)
    return new_points_event_id


def get_sum_of_points_for_user(user_id):
    db = PointsEventRepository()
    all_points_events = db.get_points_events_by_user_id(user_id)
    sum_of_points = 0
    for point_event in all_points_events:
        if point_event[0].increase:
            sum_of_points += float(point_event[0].value)
        else:
            sum_of_points -= float(point_event[0].value)
    return sum_of_points
