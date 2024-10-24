from django.db import models


###########################################
# Abstract tables - for field inheritance #
###########################################

class FactorEstimResultContainer(models.Model):
    market = models.IntegerField(blank=True, null=True)
    reversal = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    new_coin = models.FloatField(blank=True, null=True)
    momentum = models.FloatField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True


class DateIdTable(models.Model):
    id = models.AutoField(primary_key=True, default=-1)
    date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class DatePrimaryKey(models.Model):
    date = models.DateField(primary_key=True)

    class Meta:
        abstract = True


class DatePrimaryKeyWithVersionDate(DatePrimaryKey):
    version_date = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        abstract = True


class DateIdTableWithVersionDate(DateIdTable):
    version_date = models.DateField(max_length=12, blank=True, null=True)

    class Meta:
        abstract = True


class DateIdTableWithSymbol(DateIdTable):
    symbol = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


###################
# Real datatables #
###################

class RawPriceData(DateIdTableWithSymbol):
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    dividends = models.FloatField(blank=True, null=True)
    stock_splits = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "raw_price_data"
        unique_together = (("date", "symbol"),)


class Returns(DateIdTableWithSymbol):
    return_field = models.FloatField(
        db_column="return", blank=True, null=True
    )  # Field renamed because it was a Python reserved word.
    risk_free_rate = models.FloatField(blank=True, null=True)
    total_return = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "returns"
        unique_together = (("date", "symbol"),)


class RiskFreeRates(DatePrimaryKey):
    risk_free_rate = models.FloatField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "risk_free_rates"


class Exposures(FactorEstimResultContainer, DateIdTableWithSymbol):
    return_field = models.FloatField(
        db_column="return", blank=True, null=True
    )  # Field renamed because it was a Python reserved word.
    transformed_market_cap = models.FloatField(blank=True, null=True)
    core_universe = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "exposures"
        unique_together = (("date", "symbol"),)


class FactorReturns(FactorEstimResultContainer, DatePrimaryKeyWithVersionDate):
    class Meta:
        managed = False
        db_table = "factor_returns"


class RSquares(DateIdTableWithVersionDate):
    r2_core = models.FloatField(blank=True, null=True)
    r2_adj = models.FloatField(blank=True, null=True)
    nobs = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r_squares"


class SpecificReturns(DateIdTableWithSymbol):
    specific_return = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "specific_returns"
        unique_together = (("date", "symbol"),)


class TStatistics(FactorEstimResultContainer, DatePrimaryKeyWithVersionDate):
    class Meta:
        managed = False
        db_table = "t_statistics"


class Vifs(FactorEstimResultContainer, DatePrimaryKeyWithVersionDate):
    class Meta:
        managed = False
        db_table = "vifs"


class CoreSpecificRisk(DateIdTableWithVersionDate):
    half_life = models.IntegerField(blank=True, null=True)
    specific_risk = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_specific_risk"
        unique_together = (("date", "half_life"),)
