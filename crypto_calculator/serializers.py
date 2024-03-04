from rest_framework import serializers
from .models import RawPriceData


class RawPriceDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    close = serializers.FloatField()
    volume = serializers.IntegerField()
    dividends = serializers.FloatField()
    stock_splits = serializers.FloatField()
    date = serializers.DateField()
    symbol = serializers.CharField(max_length=20)

    class Meta:
        model = RawPriceData
        fields = [
            "id",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "stock_splits",
            "date",
            "symbol",
        ]
        read_only_fields = [
            "id",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "stock_splits",
            "date",
            "symbol",
        ]
