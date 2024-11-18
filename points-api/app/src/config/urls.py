from django.urls import path, include

urlpatterns = [
    path('api/v1/points/', include('src.points_event.points_event_urls')),
]