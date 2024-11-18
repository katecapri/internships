from django.urls import path, include

urlpatterns = [
    path('api/v1/auth/', include('src.auth.auth_urls')),
    path('api/v1/user/', include('src.user.user_urls')),
    path('api/v1/appRole/', include('src.app_role.app_role_urls')),
    path('api/v1/direction/', include('src.place.direction_urls')),
    path('api/v1/points/', include('src.points.points_urls')),
    path('api/v1/place/', include('src.place.place_urls')),
    path('api/v1/template/', include('src.route.template_urls')),
    path('api/v1/route/', include('src.route.route_urls')),
    path('api/v1/request/', include('src.route.request_urls')),
]
