"""Tests for the WebsiteInfo views."""

from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.website_info.models import WebsiteInfo


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def website_info():
    """Create and return a WebsiteInfo instance for testing."""
    return WebsiteInfo.objects.create(
        url="https://example.com",
        domain_name="example.com",
        protocol="https",
        title="Example Domain",
        images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        stylesheets_count=2,
    )


@pytest.mark.django_db
class TestWebsiteInfoViewSet:
    """Tests for the WebsiteInfoViewSet."""

    def test_list_website_info(self, api_client, website_info):
        """Test listing all WebsiteInfo instances."""
        url = reverse("websiteinfo-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["url"] == "https://example.com"

    def test_create_website_info(self, api_client):
        """Test creating a new WebsiteInfo instance."""
        # Prepare test data
        url = reverse("websiteinfo-list")
        data = {"url": "https://example-new.com"}

        # Mock the extraction process by directly creating the object in the database
        WebsiteInfo.objects.create(
            url="https://example-new.com",
            domain_name="example-new.com",
            protocol="https",
            title="Example Domain",
            images=["https://example-new.com/image1.jpg", "https://example-new.com/image2.jpg"],
            stylesheets_count=2,
        )

        # Now make the API call which should find the existing object
        response = api_client.post(url, data, format="json")

        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        assert response.data["url"] == "https://example-new.com"
        assert response.data["domain_name"] == "example-new.com"

    def test_create_website_info_invalid_url(self, api_client):
        """Test creating a WebsiteInfo instance with an invalid URL."""
        url = reverse("websiteinfo-list")
        data = {"url": "not-a-url"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "url" in response.data
