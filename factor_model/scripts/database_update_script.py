import sys
import os
import pandas as pd
import logging
from tqdm import tqdm
import statsmodels.api as sm
import datetime
import sqlite3


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

sys.path.insert(0, r"E:/Thesis/crypto_project")
from factor_model.model_update.loaders.crypto_coin_loaders import (
    get_extended_ticker_list,
)
from factor_model.model_update.loaders.price_data_loaders import (
    generate_ytickets,
    generate_price_data_map,
)
from factor_model.model_update.loaders.market_cap_loader import (
    generate_market_cap_only,
)
from factor_model.model_update.loaders.crypto_coin_loaders import (
    get_extended_ticker_list,
)
from statsmodels.stats.outliers_influence import variance_inflation_factor

from factor_model.model_update.return_generators.total_return_calculation import (
    generate_return_data,
)
from datetime import date, timedelta
from factor_model.model_update.database_generators.generate_databases import (
    refresh_database,
)
from factor_model.model_update.estimation_universe.estimation_core_universe import (
    generate_estimation_basis,
)
from factor_model.model_update.styles.return_based import (
    generate_x_month_price_change,
)
from factor_model.model_update.styles.volume_based import (
    generate_x_month_aggregate_volume,
)
from factor_model.model_update.factor_return_estimation.factor_return_estimation import (
    create_factor_return_data,
)
from factor_model.model_update.loaders.risk_free_rate_loader import (
    get_risk_free_rate_history,
)
from factor_model.model_update.return_generators.excess_return_calculation import (
    generate_excess_returns,
)
from factor_model.risk_calculations.core_universe_portfolio import (
    generate_market_portfolio,
)
from factor_model.risk_calculations.specific_risk import (
    generate_raw_portfolio_specific_risk,
)


DATABASE_LOCATION = r"E:/Thesis/database"
from factor_model.model_update.database_generators import (
    RAW_DATA_DB,
    RETURN_DB,
    SPECIFIC_RISK,
    FACTOR_MODEL_ESTIMATES,
    FIX_SET_OF_HALF_LIFES,
)
from factor_model.model_update import UPDATE_PARAMS, RISK_CALCULATION_PARAMETERS

parameters = UPDATE_PARAMS.copy()
parameters["CORE_UNIV_START"] = parameters["ESTIMATION_DAY"] - timedelta(
    parameters["PRESENT_IN_MARKET"]
)
parameters["GENERATE_DATABASE"] = True
parameters["HORIZON"] = "1y"  # 1y is also fair
parameters["NOBS"] = 3000
tickers = get_extended_ticker_list(
    parameters["NOBS"]
)  # the number of crypto can be adjusted...
# TODO : survival bias should be fixed by adding discontiued crypto currency
tickers = [f for f in tickers if f.endswith("USD")]
tickers = sorted(list(set(tickers)))
yfinance_tickers = generate_ytickets(tickers)
price_data_map, tickers_with_missing_data = generate_price_data_map(
    yfinance_tickers, parameters["HORIZON"]
)

problematic_keys = []
for key in price_data_map.keys():
    if len(price_data_map[key].columns) > 8:
        problematic_keys.append(key)

for key in problematic_keys:
    del price_data_map[key]

# refresh tickers and throw out those ones, which have no price history
drop_keys = list()
for key in price_data_map.keys():
    if len(price_data_map[key]) < 2:  # minimum number of obs for returns are 2
        del yfinance_tickers[key]
        drop_keys.append(key)
for key in drop_keys:
    del price_data_map[key]
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RAW_DATA_DB)) as conn:
    max_dates = pd.read_sql(
        "SELECT MAX(date) as date, symbol FROM raw_price_data group by symbol", conn
    )
max_dates_struct = max_dates.set_index("symbol").to_dict()
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RAW_DATA_DB)) as conn:
    max_id = pd.read_sql("SELECT MAX(id) as id FROM raw_price_data", conn)
idx_index = int(max_id["id"].values[0]) + 1
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RAW_DATA_DB)) as conn:
    for key in price_data_map:
        latest_date = max_dates_struct["date"].get(key, "2008-01-01")

        df_temp = price_data_map[key]
        df_temp = df_temp[df_temp["date"].astype(str) > latest_date].copy()
        df_temp["symbol"] = key
        df_temp.columns = [col.lower().replace(" ", "_") for col in df_temp.columns]
        df_temp.reset_index(inplace=True)
        df_temp.rename(columns={"index": "id"}, inplace=True)
        df_temp["id"] = range(idx_index, len(df_temp) + idx_index)
        idx_index += len(df_temp)
        df_temp.to_sql("raw_price_data", conn, if_exists="append", index=False)
# market_cap_df_full = generate_market_cap_data(yfinance_tickers)
market_cap_df = generate_market_cap_only(yfinance_tickers)
# generate square root of cap weighting
market_cap_df["transformed_market_cap"] = parameters["WEIGHT_FUNCTION"](
    market_cap_df["market_cap"]
)
market_cap_df.sort_values(by="transformed_market_cap", ascending=False, inplace=True)
total_return_data_map = generate_return_data(price_data_map)
estimation_dates = list(
    total_return_data_map["BTC-USD"].tail(parameters["ESTIMATION_HORIZON"])["date"]
)
estimation_dates = list(
    total_return_data_map["ETC-USD"].tail(parameters["ESTIMATION_HORIZON"])["date"]
)

with sqlite3.connect(os.path.join(DATABASE_LOCATION, FACTOR_MODEL_ESTIMATES)) as conn:
    max_fac_return_date = pd.read_sql(
        "SELECT MAX(date) as date FROM factor_returns", conn
    )["date"].values[0]
last_estima_date = date(
    int(max_fac_return_date[0:4]),
    int(max_fac_return_date[5:7]),
    int(max_fac_return_date[8:]),
)
estimation_dates = [
    date_value
    for date_value in estimation_dates
    if date_value > datetime.date(2018, 5, 8) and date_value > last_estima_date
]  # six months after ETH-USD has data in yfinance
estimation_dates
risk_free_rate_data = get_risk_free_rate_history(estimation_dates)
excess_return_data_map = generate_excess_returns(
    total_return_data_map, risk_free_rate_data
)
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RETURN_DB)) as conn:
    max_dates = pd.read_sql(
        "SELECT MAX(date) as date, symbol FROM returns group by symbol", conn
    )
max_dates_struct = max_dates.set_index("symbol").to_dict()
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RETURN_DB)) as conn:
    for key in excess_return_data_map:
        latest_date = max_dates_struct["date"].get(key, "2008-01-01")
        df_temp = excess_return_data_map[key]
        df_temp = df_temp[df_temp["date"].astype(str) > latest_date].copy()
        df_temp["symbol"] = key
        df_temp.columns = [col.lower().replace(" ", "_") for col in df_temp.columns]
        df_temp.reset_index(inplace=True)
        df_temp.rename(columns={"index": "id"}, inplace=True)
        df_temp["id"] = range(idx_index, len(df_temp) + idx_index)
        idx_index += len(df_temp)
        df_temp.to_sql("returns", conn, if_exists="append", index=False)
with sqlite3.connect(os.path.join(DATABASE_LOCATION, RETURN_DB)) as conn:
    max_date_risk_free = pd.read_sql(
        "SELECT MAX(date) as date FROM risk_free_rates", conn
    )["date"].values[0]
    last_estima_date = date(
        int(max_date_risk_free[0:4]),
        int(max_date_risk_free[5:7]),
        int(max_date_risk_free[8:]),
    )
    rft_sel = risk_free_rate_data[risk_free_rate_data["date"] > last_estima_date].copy()
    rft_sel["id"] = range(0, len(rft_sel))
    rft_sel.to_sql("risk_free_rates", conn, if_exists="append", index=False)
momentum_move_map = generate_x_month_price_change(
    price_data_map, x_len=6, month_len=parameters["MONTH_LENGTH"]
)
reversal_map = generate_x_month_price_change(
    price_data_map, x_len=1, month_len=parameters["MONTH_LENGTH"]
)
volume_map = generate_x_month_aggregate_volume(
    price_data_map, x_len=1, month_len=parameters["MONTH_LENGTH"]
)
daily_data_maps = {}
daily_data_maps["reversal"] = reversal_map
daily_data_maps["momentum"] = momentum_move_map
daily_data_maps["return"] = excess_return_data_map
daily_data_maps["volume"] = volume_map
tstats_all = list()
coefficients_all = list()
vif_all = list()
model_summary = list()

for date in tqdm(estimation_dates):
    # step 0 : assemble and save estimation data
    estimation_basis, _ = generate_estimation_basis(
        excess_return_data_map, market_cap_df, date, parameters
    )
    factor_return_data = create_factor_return_data(
        estimation_basis, parameters, date, daily_data_maps
    )
    factor_return_data_core = factor_return_data[
        factor_return_data["core_universe"] > 0
    ]
    if parameters["GENERATE_DATABASE"]:
        refresh_database(
            symbol_level_data={
                str(date): factor_return_data.rename(columns={"ticker": "symbol"})
            },
            database_location=DATABASE_LOCATION,
            database_name=FACTOR_MODEL_ESTIMATES,
            database_table_name="exposures",
            delete_database=False,
            key_field_name="date",
            update_mode="append",
        )
    # step 1 estimation
    try:
        mod_wls = sm.WLS(
            endog=factor_return_data_core["return"],
            exog=factor_return_data_core[parameters["REGRESSORS_SET1"]],
            weights=factor_return_data_core["transformed_market_cap"],
        ).fit()

        # step 2 save results
        coefficient_date = mod_wls.params.to_frame().T
        coefficient_date["date"] = date
        coefficients_all.append(coefficient_date)

        tstat_date = mod_wls.tvalues.to_frame().T
        tstat_date["date"] = date
        tstats_all.append(tstat_date)

        model_summary.append(
            pd.DataFrame(
                {
                    "date": [date],
                    "r2_core": [mod_wls.rsquared],
                    "r2_adj": [mod_wls.rsquared_adj],
                    "nobs": [mod_wls.nobs],
                }
            )
        )

        exog = factor_return_data[
            parameters["REGRESSORS_SET1"] + parameters["REGRESSORS_SET2"]
        ].to_numpy()
        num_features = exog.shape[1]
        vif_values = [variance_inflation_factor(exog, i) for i in range(num_features)]
        vif_result_date = (
            pd.Series(
                vif_values,
                index=parameters["REGRESSORS_SET1"] + parameters["REGRESSORS_SET2"],
            )
            .to_frame()
            .T
        )
        vif_result_date["date"] = date
        vif_all.append(vif_result_date)

        specific_returns = factor_return_data[["ticker"]].copy()
        specific_returns["specific_return"] = factor_return_data[
            "return"
        ] - mod_wls.predict(factor_return_data[parameters["REGRESSORS_SET1"]])
        if parameters["GENERATE_DATABASE"]:
            refresh_database(
                symbol_level_data={
                    str(date): specific_returns.rename(columns={"ticker": "symbol"})
                },
                database_location=DATABASE_LOCATION,
                database_name=FACTOR_MODEL_ESTIMATES,
                database_table_name="specific_returns",
                delete_database=False,
                key_field_name="date",
                update_mode="append",
            )
    except Exception:
        print(date)
all_tstat = pd.concat(tstats_all, axis=0)
all_coeff = pd.concat(coefficients_all, axis=0)
all_vif = pd.concat(vif_all, axis=0)
all_model_summary = pd.concat(model_summary, axis=0)
if parameters["GENERATE_DATABASE"]:
    refresh_database(
        symbol_level_data={str(datetime.date.today()): all_tstat},
        database_location=DATABASE_LOCATION,
        database_name=FACTOR_MODEL_ESTIMATES,
        database_table_name="t_statistics",
        delete_database=False,
        key_field_name="version_date",
        update_mode="append",
        drop_id_col=True,
    )
    refresh_database(
        symbol_level_data={str(datetime.date.today()): all_coeff},
        database_location=DATABASE_LOCATION,
        database_name=FACTOR_MODEL_ESTIMATES,
        database_table_name="factor_returns",
        delete_database=False,
        key_field_name="version_date",
        update_mode="append",
        drop_id_col=True,
    )
    refresh_database(
        symbol_level_data={str(datetime.date.today()): all_vif},
        database_location=DATABASE_LOCATION,
        database_name=FACTOR_MODEL_ESTIMATES,
        database_table_name="vifs",
        delete_database=False,
        key_field_name="version_date",
        update_mode="append",
        drop_id_col=True,
    )
    refresh_database(
        symbol_level_data={str(datetime.date.today()): all_model_summary},
        database_location=DATABASE_LOCATION,
        database_name=FACTOR_MODEL_ESTIMATES,
        database_table_name="r_squares",
        delete_database=False,
        key_field_name="version_date",
        update_mode="append",
        drop_id_col=True,
    )
# specific risk related
with sqlite3.connect(os.path.join(DATABASE_LOCATION, FACTOR_MODEL_ESTIMATES)) as conn:
    full_specific_returns = pd.read_sql_query(f"SELECT * FROM specific_returns", conn)

with sqlite3.connect(os.path.join(DATABASE_LOCATION, FACTOR_MODEL_ESTIMATES)) as conn:
    estim_universe = pd.read_sql_query(
        f"SELECT symbol, transformed_market_cap, date, core_universe FROM exposures where core_universe > 0",
        conn,
    )
full_specific_returns = full_specific_returns[
    full_specific_returns["symbol"].isin(
        list(set(estim_universe[estim_universe["core_universe"] > 0]["symbol"]))
    )
].copy()
dates = [
    date_v
    for date_v in list(full_specific_returns["date"].unique())[1:]
    if date_v in [str(d) for d in estimation_dates]
]
risk_calculation_parameters = RISK_CALCULATION_PARAMETERS.copy()


def multi_process_calc(temp_half_life):
    risk_calculation_parameters = {"specific_risk_half_life": temp_half_life}
    risk_for_half_life = full_specific_returns.groupby(
        "symbol", group_keys=False, as_index=False
    ).apply(
        lambda group: pd.DataFrame(
            {
                "date": group["date"],
                "specific_risk": group["specific_return"]
                .ewm(halflife=risk_calculation_parameters["specific_risk_half_life"])
                .std(),
            }
        )
        .reset_index(drop=False)
        .rename(columns={"index": "symbol"})
    )
    return risk_for_half_life.reset_index(drop=True)


all_core_spec_risk = {}

for temp_half_life in tqdm(FIX_SET_OF_HALF_LIFES):
    all_core_spec_risk[temp_half_life] = multi_process_calc(temp_half_life)
    all_core_spec_risk[temp_half_life].set_index(["date", "symbol"], inplace=True)
estim_universe_dict = {date: df for date, df in estim_universe.groupby("date")}
for key in all_core_spec_risk.keys():
    all_core_spec_risk[key] = {
        date: df for date, df in all_core_spec_risk[key].groupby("date")
    }
all_combined_specific_risk_estimates = list()

for date in tqdm(dates):
    # 1. gather exposures
    exposure = estim_universe_dict[date]
    # 2. identify universe_info
    market_portfolio = generate_market_portfolio(exposure)

    for half_life in FIX_SET_OF_HALF_LIFES:
        # 3. grab relevant spec risks
        tempd_df = all_core_spec_risk[half_life][date]
        tempd_df.reset_index(inplace=True)
        tempd_df.set_index("symbol", inplace=True)
        tempd_df.dropna(inplace=True)

        all_combined_specific_risk_estimates.append(
            pd.DataFrame(
                {
                    "date": [date],
                    "half_life": [half_life],
                    "specific_risk": generate_raw_portfolio_specific_risk(
                        tempd_df.to_dict()["specific_risk"], market_portfolio
                    ),
                }
            )
        )
combined_spec_risk = pd.concat(all_combined_specific_risk_estimates)
refresh_database(
    symbol_level_data={str(date): combined_spec_risk},
    database_location=DATABASE_LOCATION,
    database_name=SPECIFIC_RISK,
    database_table_name="core_specific_risk",
    delete_database=False,
    key_field_name="version_date",
    update_mode="append",
)
