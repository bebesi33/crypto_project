from django.urls import path
from . import views


app_name="crypto_calculator"
urlpatterns = [
    path("api/get_raw_price_data", views.get_raw_price_data, name='get_raw_price_data')
]
