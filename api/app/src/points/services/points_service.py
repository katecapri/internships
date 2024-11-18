from uuid import uuid4
import json

from src.points.services.points_core import EventType, PointsEventData
from src.message_broker.producer import send_into_points_queue


def prepare_points_event_info_for_queue(points_event_info: PointsEventData):
    new_points_event_data = {
        "id": str(uuid4()),
        "ownerId": str(points_event_info.user_id),
        "eventType": points_event_info.event_type,
        "pointsValue": points_event_info.points_value,
        "reason": points_event_info.reason,
    }
    send_into_points_queue(json.dumps(new_points_event_data))
