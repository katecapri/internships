import os

from src.user.services.user_service import create_admin_user
from src.user.services.user_core import CreateUserData
from src.user.services.user_repository import UserRepository

from src.app_role.services.app_role_service import get_app_role_uuid_by_code


def init_admin_user():
    admin_app_role_id = get_app_role_uuid_by_code("ADMIN")
    db = UserRepository()
    admin_user = db.has_admin_user(admin_app_role_id)
    if not admin_user:
        new_admin_user = CreateUserData(
            email=os.getenv("ACCOUNT_INIT_EMAIL"),
            name=os.getenv("ACCOUNT_INIT_EMAIL"),
            is_email_confirmed=True,
            app_role_id=admin_app_role_id,
            groups=None
        )
        create_admin_user(new_admin_user)
