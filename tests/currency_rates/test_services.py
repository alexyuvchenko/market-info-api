"""Tests for the currency_rates services."""

from unittest.mock import patch

import pytest

from apps.currency_rates.services import (
    calculate_bitcoin_price_gbp,
    get_bitcoin_price_eur,
    get_currency_rates,
    get_eur_to_gbp_rate,
)


class TestCurrencyRatesServices:
    """Tests for the currency_rates services."""

    @patch("apps.currency_rates.services.BlockchainApiClient")
    def test_get_bitcoin_price_eur(self, mock_client):
        """Test getting Bitcoin price in EUR."""
        mock_instance = mock_client.return_value
        mock_instance.get_bitcoin_price_eur.return_value = 50000.0

        result = get_bitcoin_price_eur()

        assert result == 50000.0
        mock_instance.get_bitcoin_price_eur.assert_called_once()

    @patch("apps.currency_rates.services.EcbApiClient")
    def test_get_eur_to_gbp_rate(self, mock_client):
        """Test getting EUR to GBP conversion rate."""
        mock_instance = mock_client.return_value
        mock_instance.get_eur_to_gbp_rate.return_value = 1.2

        result = get_eur_to_gbp_rate()

        assert result == 1.2
        mock_instance.get_eur_to_gbp_rate.assert_called_once()

    @patch("apps.currency_rates.services.get_bitcoin_price_eur")
    @patch("apps.currency_rates.services.get_eur_to_gbp_rate")
    def test_get_currency_rates(self, mock_get_eur_gbp, mock_get_btc_eur):
        """Test getting all currency rates."""
        mock_get_btc_eur.return_value = 50000.0
        mock_get_eur_gbp.side_effect = [1.2, 1.2]  # Called twice, for last month and today

        result = get_currency_rates()

        assert result == {"bitcoin_eur": 50000.0, "eur_to_gbp": 1.2, "bitcoin_gbp": 50000.0 / 1.2}
        mock_get_btc_eur.assert_called_once()
        assert mock_get_eur_gbp.call_count == 2
