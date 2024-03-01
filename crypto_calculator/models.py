from django.db import models


class RawPriceData(models.Model):
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    dividends = models.FloatField(blank=True, null=True)
    stock_splits = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raw_price_data'
