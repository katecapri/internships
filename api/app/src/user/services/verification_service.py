import uuid
from uuid import uuid4
from datetime import datetime

from rest_framework import serializers
from src.user.services.verification_repository import VerificationRepository
from src.user.services.user_core import VerificationCodeData


def create_verification(verification_type, user_uuid):
    code_for_verification = uuid4()
    verification_code = VerificationCodeData(
        user_id=user_uuid,
        verification_type=verification_type,
        code=code_for_verification
    )
    db = VerificationRepository()
    new_verification_code = db.create_verification(verification_code)
    return new_verification_code


def is_verification_code_valid(code):
    db = VerificationRepository()
    verification = db.get_verification_by_code(code)
    if verification and verification.expired_time > datetime.now() and verification.used_time is None:
        return code
    else:
        raise serializers.ValidationError("Verification code is expired or not exist.")


def is_csrf_valid(input_csrf, request):
    csrf_code = request.session.get('csrftoken', str(uuid.uuid4()))
    is_valid_csrf = bool(str(csrf_code) == str(input_csrf))
    if is_valid_csrf:
        return input_csrf
    else:
        raise serializers.ValidationError("Csrf code is wrong")
