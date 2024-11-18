import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid

from src.auth.services.auth_service import authenticate, generate_jwt, signup, request_password, \
    save_password, verify_email
from src.auth.serializers import SignupSerializer, LoginSerializer, \
    RequestPasswordSerializer, ResetPasswordSerializer, VerifyEmailSerializer

from src.services.decorators import request_body

logger = logging.getLogger('app')


class AuthController(viewsets.ViewSet):
    serializer_classes = {
        "signup": SignupSerializer,
        "login": LoginSerializer,
        "get_csrf_code": None,
        "verify_email": VerifyEmailSerializer,
        "request_password": RequestPasswordSerializer,
        "reset_password": ResetPasswordSerializer,
        "logout": None
    }

    @request_body(SignupSerializer)
    def signup(self, request, app_user_data):
        try:
            result = signup(app_user_data)
            if result:
                return Response(status=status.HTTP_201_CREATED)
            else:
                logger.error("Signup was not successful")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(LoginSerializer)
    def login(self, request, login_data):
        try:
            user = authenticate(login_data["login"],
                                login_data["password"])
            if not user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_email_confirmed:
                logger.error("The user's email isn`t confirmed.")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            jwt = generate_jwt(user.id)
            request.session.clear()
            request.session.flush()
            request.session["jwt"] = jwt
            return Response(data={"token": jwt}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_csrf_code(self, request):
        try:
            csrf = request.session.get('csrftoken', str(uuid.uuid4()))
            request.session['csrftoken'] = csrf
            return Response(
                data={"csrf": csrf},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(VerifyEmailSerializer)
    def verify_email(self, request, verify_email_data):
        try:
            result = verify_email(verify_email_data["code"])
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(RequestPasswordSerializer)
    def request_password(self, request, send_email_data):
        try:
            result = request_password(send_email_data["email"])
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(ResetPasswordSerializer)
    def reset_password(self, request, data_to_reset_password):
        try:
            result = save_password(
                data_to_reset_password["code"], data_to_reset_password["password"]
            )
            if result:
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        try:
            request.session.clear()
            request.session.flush()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
