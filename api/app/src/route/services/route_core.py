import enum


class RouteDateStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    no_matter = "no_matter"


class RouteType(str, enum.Enum):
    internship = "internship"
    internshipSelection = "internshipSelection"


class StepType(str, enum.Enum):
    request = "request"
    timeSheet = "timeSheet"


class FieldType(str, enum.Enum):
    string = "string"
    select = "select"
    selectWithInput = "selectWithInput"
    number = "number"
    boolean = "boolean"


class CorrectnessCriteria(str, enum.Enum):
    quality = "quality"
    range = "range"
    array = "array"


class TemplateType(str, enum.Enum):
    internship = "internship"
    internshipSelection = "internshipSelection"


class RequestStatus(str, enum.Enum):
    underConsideration = "underConsideration"
    approved = "approved"
    rejected = "rejected"


class DurationItem(str, enum.Enum):
    days = "days"
    months = "months"


class TimesheetDayType(str, enum.Enum):
    work = "work"
    dayOff = "dayOff"
    vacation = "vacation"
    ill = "ill"
