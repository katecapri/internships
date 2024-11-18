import enum
from dataclasses import dataclass


class EventType(str, enum.Enum):
    INCREASE = "increase"
    DECREASE = "decrease"


@dataclass
class PointsEventData:
    user_id: str
    event_type: str
    points_value: str
    reason: str
