"""Tests for the currency_rates views."""

from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.mark.django_db
class TestCurrencyRatesView:
    """Tests for the CurrencyRatesView."""

    def test_get_currency_rates(self, api_client):
        """Test getting currency rates."""
        with patch("apps.currency_rates.services.get_currency_rates") as mock_get_rates:
            mock_get_rates.return_value = {
                "bitcoin_eur": 50000.0,
                "eur_to_gbp": 0.7,
                "bitcoin_gbp": 50000.0 * 0.7,
            }

            url = reverse("currency-rates")
            response = api_client.get(url)

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {
                "bitcoin_eur": 50000.0,
                "eur_to_gbp": 0.7,
                "bitcoin_gbp": 50000.0 * 0.7,
            }
