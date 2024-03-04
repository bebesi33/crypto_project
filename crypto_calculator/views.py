from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd


async def get_raw_price_data(request):
    raw_price_data = await sync_to_async(list)(RawPriceData.objects.filter(symbol='BTC-USD').values())
    df = pd.DataFrame(list(raw_price_data))
    json_data = df.drop(columns=["id"]).to_dict()
    return JsonResponse(json_data)
