import pandas as pd
import numpy as np
from crypto_calculator.models import RSquares, TStatistics, Vifs


def get_vif_stats():
    field_names = [
        field.name
        for field in Vifs._meta.get_fields()
        if field.name not in ["id", "market", "version_date"]
    ]  # defer refused to work
    vifs = Vifs.objects.using("factor_model_estimates").values(*field_names)
    vifs = pd.DataFrame(list(vifs))
    last_date = max(vifs["date"])
    first_date = min(vifs["date"])
    vif_dict = {}
    for style in sorted(list(set(vifs.columns) - {"date"})):
        vif_dict[style] = np.round(
            sum(abs(vifs[style].astype(float)) > 5) / len(vifs) * 100, 1
        )
    return {
        "len": len(vifs),
        "last_date": last_date,
        "first_date": first_date,
        "problematic_ratio": vif_dict,
    }


def get_tstats_stats():
    field_names = [
        field.name
        for field in TStatistics._meta.get_fields()
        if field.name not in ["id", "version_date"]
    ]  # defer refused to work
    stats = TStatistics.objects.using("factor_model_estimates").values(*field_names)
    stats = pd.DataFrame(list(stats))
    last_date = max(stats["date"])
    first_date = min(stats["date"])
    tstat_dict = {}
    for style in sorted(list(set(stats.columns) - {"date"})):
        tstat_dict[style] = np.round(
            sum(abs(stats[style]) > 1.96) / len(stats) * 100, 1
        )
    return {
        "len": len(stats),
        "last_date": last_date,
        "first_date": first_date,
        "active_tstat_ratio": tstat_dict,
    }


def get_rsquares():
    field_names = [
        field.name
        for field in RSquares._meta.get_fields()
        if field.name not in ["id", "version_date"]
    ]  # defer refused to work
    rsquares = RSquares.objects.using("factor_model_estimates").values(*field_names)
    rsquares = pd.DataFrame(list(rsquares))
    rsquare_dict = {}
    rsquare_dict["len"] = len(rsquares)
    rsquare_dict["avg_core_r2"] = np.nanmean(rsquares["r2_core"]) * 100
    rsquare_dict["avg_core_r2_adj"] = np.nanmean(rsquares["r2_adj"]) * 100
    rsquare_dict["avg_nobs"] = np.nanmean(rsquares["nobs"])
    return rsquare_dict
