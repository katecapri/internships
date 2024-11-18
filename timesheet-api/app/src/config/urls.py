from django.urls import path, include

urlpatterns = [
    path('api/v1/timesheet/', include('src.timesheet.timesheet_urls')),
]