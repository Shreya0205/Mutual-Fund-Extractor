from django.db import models

class MutualFundFamily(models.Model):
    mutual_fund_family = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mutual_fund_family

class MutualFundScheme(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheme_code = models.CharField(max_length=50, unique=True)
    scheme_name = models.CharField(max_length=255)
    net_asset_value = models.FloatField()
    scheme_type = models.CharField(max_length=100)
    scheme_category = models.CharField(max_length=100)
    mutual_fund_family = models.ForeignKey(MutualFundFamily, on_delete=models.CASCADE)
    isin_growth = models.CharField(max_length=50)
    isin_reinvestment = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.scheme_name} ({self.scheme_code})"
