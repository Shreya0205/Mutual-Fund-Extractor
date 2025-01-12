from rest_framework import serializers
from .models import MutualFundFamily, MutualFundScheme

class MutualFundFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFundFamily
        fields = ["id", "created_at", "mutual_fund_family"]

class MutualFundSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFundScheme
        fields = [
            "created_at",
            "updated_at",
            "scheme_code",
            "scheme_name",
            "net_asset_value",
            "scheme_type",
            "scheme_category",
            "date",
            "isin_growth",
            "isin_reinvestment"
        ]
