from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path('crypto_calculator/', include('crypto_calculator.urls')),  # Include app-specific URLs
    # Add other project-wide URLs here
]
