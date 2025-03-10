from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_currency_rates


class CurrencyRatesView(APIView):
    """
    API view for retrieving currency rates information.

    Provides:
    1. Bitcoin price in EUR (15min delayed)
    2. EUR to GBP conversion rate (monthly average from ECB)
    3. Bitcoin price in GBP (calculated using the above rates)
    """

    @extend_schema(
        description="Get Bitcoin prices and currency conversion rates",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "bitcoin_eur": {
                        "type": "number",
                        "description": "Bitcoin price in EUR (15min delayed)",
                    },
                    "eur_to_gbp": {
                        "type": "number",
                        "description": "Monthly EUR to GBP conversion rate from ECB",
                    },
                    "bitcoin_gbp": {
                        "type": "number",
                        "description": "Bitcoin price in GBP (calculated)",
                    },
                },
            }
        },
    )
    def get(self, request):
        """
        Get Bitcoin prices and currency conversion rates.

        Returns:
            - bitcoin_eur: The 15min delayed Bitcoin market price in EUR
            - eur_to_gbp: Monthly conversion rate from EUR to GBP from the European Central Bank
            - bitcoin_gbp: The price from bitcoin_eur converted to GBP using the official ECB rate
        """
        # Get all currency rates
        rates = get_currency_rates()

        # Return the data
        return Response(rates)
