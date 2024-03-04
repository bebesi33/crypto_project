from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
import pandas as pd


@require_http_methods(["GET"])
async def get_raw_price_data(request):
    raw_price_data = RawPriceData.objects.filter(symbol='BTC-USD')
    df = pd.DataFrame(list(raw_price_data.values()))
    return df.drop(columns=["id"]).to_json()