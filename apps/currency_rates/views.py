from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import (
    calculate_bitcoin_price_gbp,
    get_bitcoin_price_eur,
    get_eur_to_gbp_rate,
)


class CurrencyRatesView(APIView):
    """
    API view for retrieving currency rates information.

    Provides Bitcoin price in EUR, EUR to GBP conversion rate, and Bitcoin price in GBP.
    """

    def get(self, request):
        """
        Get Bitcoin price in EUR, EUR to GBP conversion rate, and Bitcoin price in GBP.

        Returns:
            - bitcoin_eur: The 15min delayed bitcoin market price in EUR
            - eur_to_gbp: Monthly conversion rate from EUR to GBP from the European Central Bank
            - bitcoin_gbp: The price from bitcoin_eur converted to GBP using the official ECB rate
        """
        # Get Bitcoin price in EUR

        bitcoin_eur = get_bitcoin_price_eur()

        # Get EUR to GBP conversion rate
        eur_to_gbp = get_eur_to_gbp_rate()

        # Calculate Bitcoin price in GBP
        bitcoin_gbp = calculate_bitcoin_price_gbp(bitcoin_eur, eur_to_gbp)

        # Return the data
        return Response(
            {"bitcoin_eur": bitcoin_eur, "eur_to_gbp": eur_to_gbp, "bitcoin_gbp": bitcoin_gbp}
        )
