from datetime import datetime

import requests

from funds.models import MutualFundScheme

from mutual_fund import settings


class RapidAPIClient:

    BASE_URL = settings.RAPID_API_BASE_URL
    HEADERS = {
        "x-rapidapi-key": settings.RAPID_API_TOKEN,
        "x-rapidapi-host": settings.RAPID_API_HOST
    }

    @staticmethod
    def fetch_open_ended_schemes(mutual_fund_family, scheme_type="Open Ended Schemes"):
        """
        Fetch schemes for a given mutual fund family from the external API.
        """
        querystring = {
            "Mutual_Fund_Family": mutual_fund_family,
            "Scheme_Type": scheme_type
        }
        try:
            response = requests.get(
                RapidAPIClient.BASE_URL,
                headers=RapidAPIClient.HEADERS,
                params=querystring
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Failed to fetch schemes: {str(e)}"}



class MutualFundService:

    @staticmethod
    def fetch_open_ended_schemes_for_family(mutual_fund_family: str):
        """
        Fetch mutual fund schemes using the RapidAPI client.
        """
        return RapidAPIClient.fetch_open_ended_schemes(mutual_fund_family)

    @staticmethod
    def save_schemes_to_db(mutual_fund_family, schemes_data):
        """
        Save the fetched mutual fund schemes to the database.
        """
        try:
            # Save the fetched schemes to the database
            for scheme in schemes_data.get("data"):
                MutualFundScheme.objects.update_or_create(
                    scheme_code=scheme.get("Scheme_Code"),
                    mutual_fund_family=mutual_fund_family,
                    defaults={
                        "scheme_name": scheme.get("Scheme_Name"),
                        "net_asset_value": scheme.get("Net_Asset_Value"),
                        "scheme_type": scheme.get("Scheme_Type"),
                        "scheme_category": scheme.get("Scheme_Category"),
                        "date": datetime.strptime(scheme.get("Date"),"%d-%b-%Y").strftime("%Y-%m-%d"),
                        "isin_growth": scheme.get("ISIN_Div_Payout_ISIN_Growth"),
                        "isin_reinvestment": scheme.get("ISIN_Div_Reinvestment", ""),
                    },
                )

            return {"success": True, "message": f"Schemes for {mutual_fund_family.mutual_fund_family} fetched and saved successfully."}

        except Exception as e:
            return {"success": False, "error": f"Failed to save schemes: {str(e)}"}
