from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", TemplateView.as_view(template_name="index.html")),
    path('crypto/', include('crypto_calculator.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html"))  # the ordering matters
]
