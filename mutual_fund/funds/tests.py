from unittest import mock
from urllib.parse import urlencode

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch


class MutualFundFamilyTestCase(APITestCase):

    def setUp(self):
        self.mock_data = {
            "success": True,
            "data": [
                {
                    "Scheme_Code": 128628,
                    "ISIN_Div_Payout_ISIN_Growth": "INF179KA1JC4",
                    "ISIN_Div_Reinvestment": "-",
                    "Scheme_Name": "HDFC Banking and PSU Debt Fund - Growth Option",
                    "Net_Asset_Value": 22.0467,
                    "Date": "10-Jan-2025",
                    "Scheme_Type": "Open Ended Schemes",
                    "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
                    "Mutual_Fund_Family": "HDFC Mutual Fund"
                },
                {
                    "Scheme_Code": 128629,
                    "ISIN_Div_Payout_ISIN_Growth": "INF179KA1IZ7",
                    "ISIN_Div_Reinvestment": "-",
                    "Scheme_Name": "HDFC Banking and PSU Debt Fund - Growth Option - Direct Plan",
                    "Net_Asset_Value": 22.9155,
                    "Date": "10-Jan-2025",
                    "Scheme_Type": "Open Ended Schemes",
                    "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
                    "Mutual_Fund_Family": "HDFC Mutual Fund"
                }
            ]
        }

        self.mutual_fund_family = "HDFC Mutual Fund"
        patcher = patch('funds.services.RapidAPIClient.fetch_open_ended_schemes',
                        return_value=self.mock_data)
        self.mock_fetch_schemes = patcher.start()
        self.addCleanup(patcher.stop)

        self.register_data = {
            "email": "shreya@shreya.com",
            "password": "password",
            "username": "shreya"
        }
        self.client.post(reverse('register'), self.register_data)

        login_data = {
            "email": "shreya@shreya.com",
            "password": "password"
        }

        response = self.client.post(reverse('login'), login_data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data.get("access")}')

    def test_register_mutual_fund_family(self):

        data = {
            "mutual_fund_family":  self.mutual_fund_family
        }

        response = self.client.post(reverse('mutual-fund-families-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('mutual-fund-families-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Mutual Fund Family is already registered")

    def test_list_mutual_fund_families(self):
        data = {
            "mutual_fund_family": self.mutual_fund_family
        }

        self.client.post(reverse('mutual-fund-families-list'), data)
        response = self.client.get(reverse('mutual-fund-families-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.mutual_fund_family, [family["mutual_fund_family"] for family in response.data])

    def test_fetch_mutual_fund_schemes(self):
        family_data = {
            "mutual_fund_family": self.mutual_fund_family
        }
        self.client.post(reverse('mutual-fund-families-list'), family_data)
        query_params = {"mutual_fund_family": "HDFC Mutual Fund"}
        url = f"{reverse('mutual-fund-families-schemes')}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_missing_mutual_fund_family_parameter(self):
        response = self.client.get(reverse('mutual-fund-families-schemes'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Fund Family parameter is required")

    @patch('funds.services.RapidAPIClient.fetch_open_ended_schemes')
    def test_fetch_schemes_internal_server_error(self, mock_fetch_schemes):
        mock_fetch_schemes.return_value = {
            "success": False,
            "error": "Failed to fetch schemes: Internal server error"
        }

        family_data = {
            "mutual_fund_family": self.mutual_fund_family
        }
        self.client.post(reverse('mutual-fund-families-list'), family_data)
        query_params = {"mutual_fund_family": self.mutual_fund_family}
        url = f"{reverse('mutual-fund-families-schemes')}?{urlencode(query_params)}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Mutual Fund family not registered.")
