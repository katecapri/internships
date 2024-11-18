from django.urls import path

from src.route.controllers.template import TemplateController

urlpatterns = [
    path('', TemplateController.as_view({'get': 'get_templates', 'post': 'create_template'})),
    path('<uuid:pk>/', TemplateController.as_view({'get': 'get_template', 'post': 'update_template'})),
    path('<uuid:pk>/launch/', TemplateController.as_view({'post': 'launch_template'})),
]
