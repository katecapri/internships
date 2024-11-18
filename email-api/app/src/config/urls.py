from django.urls import path, include

urlpatterns = [
    path('api/v1/email/', include('src.email.email_urls')),
]