"""API clients for external services."""

import datetime

import requests
from django.core.cache import cache
from requests.exceptions import RequestException


class BaseApiClient:
    """Base class for API clients."""

    BASE_URL = None

    def __init__(self, timeout=30):
        """
        Initialize the API client.

        Args:
            timeout (int): Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json",
            }
        )

    def _make_request(self, endpoint, method="GET", params=None, data=None):
        """
        Make an HTTP request to the API.

        Args:
            endpoint (str): API endpoint to call
            method (str): HTTP method (GET, POST, etc.)
            params (dict): Query parameters
            data (dict): Request body for POST/PUT requests

        Returns:
            dict: JSON response data
            None: If there was an error
        """
        if not self.BASE_URL:
            raise ValueError("BASE_URL must be defined in the subclass")

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method, url=url, params=params, json=data, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response from {url}: {e}")
            return None


class BlockchainApiClient(BaseApiClient):
    """Client for interacting with the Blockchain.com API."""

    BASE_URL = "https://blockchain.info"

    def get_bitcoin_price_eur(self):
        """
        Get the current Bitcoin price in EUR.

        Returns:
            float: Bitcoin price in EUR
            None: If there was an error
        """
        ticker_data = self._make_request("ticker")
        if not ticker_data or "EUR" not in ticker_data:
            return None

        try:
            # Extract the 15min delayed price in EUR
            return float(ticker_data["EUR"]["15m"])
        except (KeyError, ValueError) as e:
            print(f"Error extracting EUR price from ticker data: {e}")
            return None


class EcbApiClient(BaseApiClient):
    """Client for interacting with the European Central Bank API."""

    BASE_URL = "https://data-api.ecb.europa.eu/service/data"

    def get_eur_to_gbp_rate(self, date_range=None):
        """
        Get the monthly EUR to GBP conversion rate from the ECB API.

        This fetches the exchange rate for the last month.

        Returns:
            float: EUR to GBP conversion rate
            None: If there was an error
        """
        try:
            # Construct the API URL
            # EXR = Exchange Rate dataset
            # M = Monthly frequency
            # GBP.EUR = Currency pair (GBP against EUR)
            # SP00 = Spot rate
            # A = Average
            endpoint = "EXR/M.GBP.EUR.SP00.A"

            params = {
                "format": "jsondata",
                "detail": "dataonly",
            }

            if date_range is not None:
                params = params | {
                    "startPeriod": date_range.get("start_date"),
                    "endPeriod": date_range.get("end_date"),
                }
            else:
                date_range = {}

            today = datetime.date.today().strftime("%Y-%m-%d")
            cache_key = f"ecb_eur_gbp_rate_{date_range.get('start_date', today)}_{date_range.get('end_date', today)}"
            eur_to_gbp_rate = cache.get(cache_key)
            if eur_to_gbp_rate is not None:
                return eur_to_gbp_rate

            data = self._make_request(endpoint, params=params)
            if not data:
                return None
            # Extract the exchange rate from the response
            observations = (
                data.get("dataSets", [{}])[0]
                .get("series", {})
                .get("0:0:0:0:0", {})
                .get("observations", {})
            )
            if observations and "0" in observations:
                # The rate is GBP to EUR, so we need to take the reciprocal to get EUR to GBP
                gbp_to_eur_rate = float(observations["0"][0])
                eur_to_gbp_rate = 1 / gbp_to_eur_rate
                cache.set(cache_key, eur_to_gbp_rate, 3600 * 24)  # caching result for 24 hours

                return eur_to_gbp_rate

            return None
        except (KeyError, ValueError, ZeroDivisionError) as e:
            print(f"Error extracting EUR to GBP rate: {e}")
            return None
