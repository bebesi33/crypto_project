from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("crypto/", include("crypto_calculator.urls")),
    re_path(
        r"^.*$", TemplateView.as_view(template_name="index.html")
    ),  # the ordering matters
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
