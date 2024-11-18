import logging
import os
from datetime import datetime, timedelta
from uuid import UUID

import jwt

from src.user.services.manager_service import send_reset_password_email, send_confirm_email_email
from src.auth.services.password_service import encrypt_password, check_password
from src.app_role.services.app_role_service import get_app_role_uuid_by_code
from src.user.services.verification_service import create_verification
from src.user.services.verification_repository import VerificationRepository
from src.user.services.user_service import create_user, get_group_by_name
from src.user.services.user_core import CreateUserData, VerificationType
from src.user.services.user_repository import UserRepository

logger = logging.getLogger('app')


def authenticate(login: str, password: str):
    db = UserRepository()
    user = db.get_user_by_email(login)

    if not user:
        return None
    result = check_password(password, str.encode(user.password))
    if not result:
        return None

    return user


def generate_jwt(user_id):
    payload = dict()
    payload["type"] = "access_token"
    payload["exp"] = datetime.now() + timedelta(
        minutes=int(os.getenv("API_JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    payload["iat"] = datetime.now()
    payload["sub"] = str(user_id)

    return jwt.encode(payload, os.getenv("API_JWT_SECRET"),
                      algorithm=os.getenv("API_JWT_ALGORITHM"))


def signup(user_info):
    encrypted_password = encrypt_password(user_info["password"])
    new_user_info = CreateUserData(
        email=user_info["email"],
        name=user_info["name"],
        is_email_confirmed=False,
        app_role_id=get_app_role_uuid_by_code("APP_USER"),
        password=encrypted_password.decode(),
        groups=[{"id": get_group_by_name('Кандидат').id}]
    )
    new_user_uuid = create_user(new_user_info)
    if not new_user_uuid:
        return None
    verification_code = create_verification(VerificationType.EMAIL, new_user_uuid)
    send_confirm_email_email(user_info["email"], verification_code)
    return new_user_uuid


def verify_email(code: UUID):
    db_verification = VerificationRepository()
    verification = db_verification.get_verification_by_code(code)
    db_user = UserRepository()
    user = db_user.verify_email(verification.user_id)
    return user


def request_password(email):
    db = UserRepository()
    user = db.get_user_by_email(email)
    if not user:
        logger.error("User was not found")
        return None
    verification_code = create_verification(VerificationType.RESET_PASSWORD, user.id)
    is_sent = send_reset_password_email(email, verification_code)
    return is_sent


def save_password(code: UUID, password: str):
    db_verification = VerificationRepository()
    verification = db_verification.get_verification_by_code(code)
    encrypted_password = encrypt_password(password)
    db_user = UserRepository()
    updated_user = db_user.update_user_password(verification.user_id, encrypted_password.decode())
    db_verification.update_verification_used_time_by_id(verification.id)
    return updated_user


