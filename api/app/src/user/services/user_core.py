import enum
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


class VerificationType(str, enum.Enum):
    RESET_PASSWORD = "RESET_PASSWORD"
    EMAIL = "EMAIL"


class RestrictedGroupType(str, enum.Enum):
    APP_ROLE = "APP_ROLE"


@dataclass
class CreateUserData:
    email: str
    name: str
    is_email_confirmed: bool
    app_role_id: str
    groups: Optional[list]
    password: str = None


@dataclass
class VerificationCodeData:
    user_id: UUID
    verification_type: VerificationType
    code: str

