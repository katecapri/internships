import logging

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('app')


def request_body(input_serializer):
    def decorator(method_to_decorate):
        def wrapper(self, request, *args, **kwargs):
            try:
                serializer = input_serializer(
                    data=request.data,
                    context={'request': request}
                )
                if not request.data and request.query_params:
                    serializer = input_serializer(
                        data=request.query_params,
                        context={'request': request}
                    )
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                logger.error(e, exc_info=True)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return method_to_decorate(self, request, serializer.data, *args, **kwargs)

        return wrapper

    return decorator
