from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
async def get_raw_price_data(request):
    print(request.body.inputValue)
    if request.method == "POST":
        raw_price_data = await sync_to_async(list)(RawPriceData.objects.filter(symbol='BTC-USD').values())
        df = await pd.DataFrame(list(raw_price_data))
        json_data = await df.drop(columns=["id"]).to_dict()
        return JsonResponse(json_data)
    else:
        return JsonResponse({})


async def get_available_symbols(request):
    symbols = await sync_to_async(list)(RawPriceData.objects.values("symbol").distinct())
    df = pd.DataFrame(list(symbols))
    json_data = df.to_dict()
    return JsonResponse(json_data)
