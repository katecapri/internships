import enum
from dataclasses import dataclass


class EventType(str, enum.Enum):
    INCREASE = "increase"
    DECREASE = "decrease"


@dataclass
class PointsEventData:
    id: str
    owner_id: str
    increase: bool
    value: str
    reason: str
