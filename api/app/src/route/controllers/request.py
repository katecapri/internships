import logging
import os

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.route.services.route_service import get_page_of_requests, create_request, \
    get_request_verification_by_request_id, verify_request
from src.route.serializers import CreateRequestSerializer
from src.services.permission_service import EntryPoint, PermissionType, has_user_permission
from src.services.decorators import request_body

logger = logging.getLogger('app')


class RequestController(viewsets.ViewSet):
    serializer_classes = {
        "read_user_requests": None,
        "create_request": CreateRequestSerializer,
        "get_request_status": None,
        "verify_request": None,
    }

    def read_user_requests(self, request):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            can_user_view_all = has_user_permission(
                request.hackathonUser.app_role, PermissionType.VIEW_ALL, EntryPoint.REQUEST)
            input_params = request.GET.keys()
            offset = int(request.GET["offset"]) if "offset" in input_params else 1
            limit = int(request.GET["limit"]) if "limit" in input_params else 5
            if can_user_view_all:
                result = get_page_of_requests(offset, limit)
            else:
                result = get_page_of_requests(offset, limit, request.hackathonUser.id)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(CreateRequestSerializer)
    def create_request(self, request, create_request_data):
        try:
            if not hasattr(request, "hackathonUser"):
                logger.error('User must be authorized for this method')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            new_request = create_request(create_request_data, request.hackathonUser.id)
            if not new_request:
                logger.error('Request was not created')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_request_status(self, request, pk):
        try:
            request_verification = get_request_verification_by_request_id(pk)
            if not request_verification:
                logger.error('Request verification was not found')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = {
                "verificationDate": request_verification.creation_date.date(),
                "isCorrect": request_verification.is_correct,
                "verificationAnswer": request_verification.verification_error
            }
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def verify_request(self, request, pk):
        try:
            if request.headers["API_CONSUMER_KEY"] == os.getenv("API_CONSUMER_KEY"):
                verify_request(pk)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
