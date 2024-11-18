import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.route.services.route_service import get_templates, get_template_by_id, \
    create_template, update_template, convert_template_to_representation, \
    check_groups_correct_after_updating, launch_template, convert_route_to_representation
from src.route.serializers import CreateTemplateSerializer, UpdateTemplateSerializer, LaunchTemplateSerializer
from src.services.decorators import request_body

logger = logging.getLogger('app')


class TemplateController(viewsets.ViewSet):
    serializer_classes = {
        "get_templates": None,
        "create_template": CreateTemplateSerializer,
        "get_template": None,
        "update_template": UpdateTemplateSerializer,
        "launch_template": LaunchTemplateSerializer
    }

    def get_templates(self, request):
        try:
            templates = get_templates()
            result = [
                {
                    "id": template.id,
                    "templateType": template.template_type,
                    "fromGroup": template.from_group,
                    "toGroup": template.to_group
                } for template in templates]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(CreateTemplateSerializer)
    def create_template(self, request, create_template_data):
        try:
            new_template = create_template(create_template_data)
            if not new_template:
                logger.error('Template was not created')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_template_to_representation(new_template)
            return Response(data=result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_template(self, request, pk):
        try:
            template = get_template_by_id(pk)
            if not template:
                logger.error('Template with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_template_to_representation(template)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(UpdateTemplateSerializer)
    def update_template(self, request, data_to_update_template, pk):
        try:
            template = get_template_by_id(pk)
            if not template:
                logger.error('Template with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if any([data_to_update_template["fromGroup"], data_to_update_template["toGroup"]]):
                if not check_groups_correct_after_updating(template, data_to_update_template):
                    logger.error('After updating, the groups will not belong to the same role')
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            if not any([data_to_update_template["templateType"], data_to_update_template["fromGroup"],
                        data_to_update_template["toGroup"], data_to_update_template["templateSteps"] is not None]):
                logger.error('One of the fields must be filled')
                return Response(status=status.HTTP_400_BAD_REQUEST)

            result = update_template(pk, data_to_update_template)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error('Template was not updated')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @request_body(LaunchTemplateSerializer)
    def launch_template(self, request, launch_template_data, pk):
        try:
            template = get_template_by_id(pk)
            if not template:
                logger.error('Template with such id does not exist')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            route = launch_template(template, launch_template_data)
            if not route:
                logger.error('Route was not created')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = convert_route_to_representation(route)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
