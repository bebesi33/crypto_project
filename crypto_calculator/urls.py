from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path("crypto_calculator/", include("crypto_calculator.urls")),
    path("admin/", admin.site.urls),
]