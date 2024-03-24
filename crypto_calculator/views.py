from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def get_raw_price_data(request):
    print(request.method)
    if request.method == "POST":
        all_input = json.loads(request.body.decode('utf-8'))
        raw_price_data = RawPriceData.objects.filter(symbol=all_input["symbol"]).values("close", "date")
        df = pd.DataFrame(list(raw_price_data))
        df["date"] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        if len(df) > 0:
            json_data = {"raw_price": df.to_dict()}
            return JsonResponse(json_data)
    # default return
    return {"ERROR_CODE": 404}


async def get_available_symbols(request):
    symbols = await sync_to_async(list)(RawPriceData.objects.values("symbol").distinct())
    df = pd.DataFrame(list(symbols))
    json_data = df.to_dict()
    return JsonResponse(json_data)
