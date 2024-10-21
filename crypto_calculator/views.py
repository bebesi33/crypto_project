from django.http import JsonResponse
from crypto_calculator.factor_return_stats_requests import (
    get_rsquares,
    get_tstats_stats,
    get_vif_stats,
)
from crypto_calculator.models import RawPriceData
from asgiref.sync import sync_to_async
import pandas as pd
from django.views.decorators.csrf import ensure_csrf_cookie
from crypto_calculator.explorer_request_processing import (
    assemble_price_data,
    decode_explorer_input,
    get_ewma_estimates,
    get_total_return,
)
from crypto_calculator.risk_calc_request_processing import (
    decode_risk_calc_input,
    risk_calc_request_full,
    risk_calc_request_reduced,
)


@ensure_csrf_cookie
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
                mean_to_zero=all_input.get("mean_to_zero"),
            )
        else:
            # if no close price, throw and error
            json_data["ERROR_CODE"] = 404
            log_elements.append(f"No price data for {symbol}!")

        json_data["log"] = " ".join(log_elements)
        return JsonResponse(json_data)
    # default return
    return JsonResponse({"ERROR_CODE": 404, "log": "404 Not Found"})


@ensure_csrf_cookie
def get_risk_calculation_output(request):
    if request.method == "POST":
        processed_input, log_elements, override_code = decode_risk_calc_input(request)

        if override_code != 404 and processed_input["use_factors"]:
            json_data = risk_calc_request_full(
                portfolio_details=processed_input["portfolio"],
                market_portfolio=processed_input["market"],
                risk_calculation_parameters=processed_input,
            )
        elif override_code != 404 and not processed_input["use_factors"]:
            json_data = risk_calc_request_reduced(
                portfolio_details=processed_input["portfolio"],
                market_portfolio=processed_input["market"],
                risk_calculation_parameters=processed_input,
            )
        else:
            json_data = {}
        json_data["log"] = log_elements
        json_data["ERROR_CODE"] = override_code
        return JsonResponse(json_data)
    # default return
    return JsonResponse({"ERROR_CODE": 404, "log": "404 Not Found"})


@ensure_csrf_cookie
def get_factor_return_stats(request):
    if request.method == "GET":
        json_data = {}
        json_data["vifs"] = get_vif_stats()
        json_data["tstats"] = get_tstats_stats()
        json_data["rsquares"] = get_rsquares()
        return JsonResponse(json_data)
    else:
        return JsonResponse({})


@ensure_csrf_cookie
async def get_available_symbols(request):
    symbols = await sync_to_async(list)(
        RawPriceData.objects.values("symbol").distinct()
    )
    df = pd.DataFrame(list(symbols))
    json_data = df.to_dict()
    return JsonResponse(json_data)
