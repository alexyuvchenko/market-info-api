"""Tests for the WebsiteInfo models."""

import pytest

from apps.website_info.models import WebsiteInfo


@pytest.mark.django_db
class TestWebsiteInfoModel:
    """Tests for the WebsiteInfo model."""

    def test_create_website_info(self):
        """Test creating a WebsiteInfo instance."""
        website_info = WebsiteInfo.objects.create(
            url="https://example.com",
            domain_name="example.com",
            protocol="https",
            title="Example Domain",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            stylesheets_count=2,
        )

        assert website_info.url == "https://example.com"
        assert website_info.domain_name == "example.com"
        assert website_info.protocol == "https"
        assert website_info.title == "Example Domain"
        assert len(website_info.images) == 2
        assert website_info.stylesheets_count == 2
        assert website_info.created_at is not None
        assert website_info.updated_at is not None
