"""Tests for the currency rates API clients."""

from unittest.mock import patch

from apps.currency_rates.clients import BlockchainApiClient, EcbApiClient


class TestBlockchainApiClient:
    """Tests for the BlockchainApiClient."""

    def test_get_bitcoin_price_eur(self):
        """Test getting Bitcoin price in EUR."""
        with patch("apps.currency_rates.clients.BlockchainApiClient._make_request") as mock_request:
            mock_request.return_value = {"EUR": {"15m": 50000.0}}

            client = BlockchainApiClient()
            result = client.get_bitcoin_price_eur()

            assert result == 50000.0
            mock_request.assert_called_once_with("ticker")

    @patch("apps.currency_rates.clients.BlockchainApiClient._make_request")
    def test_get_bitcoin_price_eur_no_data(self, mock_request):
        """Test error handling when no ticker data is available."""
        # Mock the ticker data to be None
        mock_request.return_value = None

        # Call the method
        client = BlockchainApiClient()
        result = client.get_bitcoin_price_eur()

        # Verify the result
        assert result is None

        # Verify the request was called
        mock_request.assert_called_once()

    @patch("apps.currency_rates.clients.BlockchainApiClient._make_request")
    def test_get_bitcoin_price_eur_missing_currency(self, mock_request):
        """Test error handling when EUR is not in the ticker data."""
        # Mock the ticker data without EUR
        mock_request.return_value = {"USD": {"15m": 60000.0}}

        # Call the method
        client = BlockchainApiClient()
        result = client.get_bitcoin_price_eur()

        # Verify the result
        assert result is None

        # Verify the request was called
        mock_request.assert_called_once()


class TestEcbApiClient:
    """Tests for the EcbApiClient."""

    def test_get_eur_to_gbp_rate(self):
        """Test getting EUR to GBP conversion rate."""
        with patch("apps.currency_rates.clients.EcbApiClient._make_request") as mock_request:
            mock_request.return_value = {
                "dataSets": [
                    {"series": {"0:0:0:0:0": {"observations": {"0": [0.7]}}}}  # GBP to EUR rate
                ]
            }

            client = EcbApiClient()
            result = client.get_eur_to_gbp_rate()

            assert result == 1 / 0.7  # EUR to GBP rate is reciprocal
            mock_request.assert_called_once()
