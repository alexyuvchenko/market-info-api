"""Tests for the WebsiteInfo serializers."""

import pytest

from apps.website_info.models import WebsiteInfo
from apps.website_info.serializers import URLValidator, WebsiteInfoSerializer


class TestURLValidator:
    """Tests for the URLValidator serializer."""

    def test_valid_url(self):
        """Test that a valid URL passes validation."""
        serializer = URLValidator(data={"url": "https://example.com"})
        assert serializer.is_valid()

    def test_invalid_url(self):
        """Test that an invalid URL fails validation."""
        serializer = URLValidator(data={"url": "not-a-url"})
        assert not serializer.is_valid()
        assert "url" in serializer.errors


@pytest.mark.django_db
class TestWebsiteInfoSerializer:
    """Tests for the WebsiteInfoSerializer."""

    def test_serialization(self):
        """Test serializing a WebsiteInfo instance."""
        website_info = WebsiteInfo.objects.create(
            url="https://example.com",
            domain_name="example.com",
            protocol="https",
            title="Example Domain",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            stylesheets_count=2,
        )
        serializer = WebsiteInfoSerializer(website_info)
        data = serializer.data

        assert data["url"] == "https://example.com"
        assert data["domain_name"] == "example.com"
        assert data["protocol"] == "https"
        assert data["title"] == "Example Domain"
        assert len(data["images"]) == 2
        assert data["stylesheets_count"] == 2
