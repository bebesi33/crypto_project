from django.urls import path
from . import views


app_name="crypto_calculator"
urlpatterns = [
    path("api/get_raw_price_data", views.get_raw_price_data, name='get_raw_price_data'),
    path("api/get_available_symbols", views.get_available_symbols, name='get_available_symbols')
]
