import enum


class DayType(str, enum.Enum):
    work = "work"
    dayOff = "dayOff"
    vacation = "vacation"
    ill = "ill"


class EventType(str, enum.Enum):
    generate = "generate"
    update = "update"


class DurationItem(str, enum.Enum):
    days = "days"
    months = "months"
