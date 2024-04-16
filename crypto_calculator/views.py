from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json
from crypto_calculator.sample_risk_input import market_portfolio, portfolio_details
from crypto_calculator.explorer_request_processing import (
    decode_explorer_input,
    get_close_data,
    get_ewma_estimates,
    get_total_return,
)
from crypto_calculator.risk_calc_request_processing import (
    decode_risk_calc_input,
    risk_calc_request_full,
)
from factor_model.risk_calculations.simple_risk_calculation import (
    create_ewma_std_estimates,
)
from crypto_calculator.sample_risk_input import (
    portfolio_details,
    market_portfolio,
    risk_calculation_parameters,
)


@csrf_exempt
def get_raw_price_data(request):
    if request.method == "POST":

        all_input, log_elements, override_code = decode_explorer_input(request)

        # handle raw price data
        symbol = all_input.get("symbol")
        if symbol is not None:
            close_price = get_close_data(symbol=symbol)
        else:
            close_price = pd.DataFrame()
            log_elements.append(
                "The symbol is not recognized, no data is queried from the database!"
            )
        json_data = {"raw_price": close_price.to_dict(), "symbol": symbol}

        if len(close_price) > 0:
            # if close price exists create ewma estimates and returns
            returns = get_total_return(symbol=symbol)
            halflife = all_input.get("halflife")
            min_periods = all_input.get("min_obs")
            get_ewma_estimates(
                halflife, min_periods, override_code, json_data, log_elements, returns
            )
        else:
            # if no close price, throw and error
            json_data["ERROR_CODE"] = 404
            log_elements.append(f"No price data for {symbol}!")

        json_data["log"] = " ".join(log_elements)
        return JsonResponse(json_data)
    # default return
    return {"ERROR_CODE": 404, "log": "404 Not Found"}


@csrf_exempt
def get_risk_calculation_output(request):
    processed_input, log_elements, override_code = decode_risk_calc_input(request)
    print(log_elements)
    json_data = {}
    if request.method == "POST":
        print("start risk_calc_request_full")
        json_data = risk_calc_request_full(
            portfolio_details=portfolio_details,
            market_portfolio=market_portfolio,
            risk_calculation_parameters=risk_calculation_parameters,
        )
        return JsonResponse(json_data)
    # default return
    return {"ERROR_CODE": 404, "log": "404 Not Found"}


async def get_available_symbols(request):
    symbols = await sync_to_async(list)(
        RawPriceData.objects.values("symbol").distinct()
    )
    df = pd.DataFrame(list(symbols))
    json_data = df.to_dict()
    return JsonResponse(json_data)
