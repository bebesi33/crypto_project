from django.http import JsonResponse
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json
from crypto_calculator.sample_risk_input import market_portfolio, portfolio_details
from crypto_calculator.explorer_request_processing import (
    assemble_price_data,
    decode_explorer_input,
    get_close_data,
    get_ewma_estimates,
    get_total_return,
    query_explorer_factor_return_data,
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

        all_input, log_elements, override_code, is_factor = decode_explorer_input(
            request
        )

        # handle raw price data and identify styles
        symbol = all_input.get("symbol")
        close_price, symbol = assemble_price_data(symbol, is_factor, log_elements)
        json_data = {"raw_price": close_price.to_dict(), "symbol": symbol.upper()}

        if len(close_price) > 0:
            # if close price exists create ewma estimates and returns
            returns = get_total_return(symbol, close_price, is_factor)
            get_ewma_estimates(
                all_input.get("halflife"),
                all_input.get("min_obs"),
                override_code,
                json_data,
                log_elements,
                returns,
                mean_to_zero=all_input.get("mean_to_zero")
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
    if request.method == "POST":
        processed_input, log_elements, override_code = decode_risk_calc_input(request)
        json_data = risk_calc_request_full(
            portfolio_details=processed_input["portfolio"],
            market_portfolio=processed_input["market"],
            risk_calculation_parameters=processed_input,
        )
        # json_data = risk_calc_request_full(
        #     portfolio_details=portfolio_details,
        #     market_portfolio=market_portfolio,
        #     risk_calculation_parameters=risk_calculation_parameters,
        # )
        json_data["log"] = log_elements
        json_data["ERROR_CODE"] = override_code
        print(json_data)
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
