from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json
from crypto_calculator.request_processing import get_close_data, get_return_data
from factor_model.risk_calculations.simple_risk_calculation import create_ewma_std_estimates


@csrf_exempt
def get_raw_price_data(request):
    print(request.method)
    if request.method == "POST":
        all_input = json.loads(request.body.decode("utf-8"))

        # handle raw price data
        close_price = get_close_data(symbol=all_input["symbol"])

        if len(close_price) > 0:
            # handle return data and calculate ewma risk
            returns = get_return_data(symbol=all_input["symbol"])
            ewma_std = create_ewma_std_estimates(returns, halflife=20, min_periods=20)
            ewma_std.rename(columns= {"total_return": "ewma_std"}, inplace=True)
            # align ouput length
            returns = returns[returns.index.isin(ewma_std.index)].copy()
            json_data = {
                "raw_price": close_price.to_dict(),
                "symbol": all_input["symbol"],
                "ERROR_CODE": 0,
                "return_data": returns.to_dict(),
                "ewma": ewma_std.to_dict()
            }
            return JsonResponse(json_data)
    # default return
    return {"ERROR_CODE": 404}


async def get_available_symbols(request):
    symbols = await sync_to_async(list)(
        RawPriceData.objects.values("symbol").distinct()
    )
    df = pd.DataFrame(list(symbols))
    json_data = df.to_dict()
    return JsonResponse(json_data)
