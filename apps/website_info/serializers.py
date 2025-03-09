from urllib.parse import urlparse

import validators
from rest_framework import serializers

from .models import WebsiteInfo


class URLValidator(serializers.Serializer):
    """Serializer for validating URLs."""

    url = serializers.CharField(max_length=2048)

    def validate_url(self, value):
        """Validate that the input is a valid URL."""
        if not validators.url(value):
            raise serializers.ValidationError("Invalid URL format.")
        return value


class WebsiteInfoSerializer(serializers.ModelSerializer):
    # Explicitly define images as a ListField to ensure proper OpenAPI schema
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        help_text="List of image URLs found on the website",
    )

    class Meta:
        model = WebsiteInfo
        fields = [
            "id",
            "url",
            "domain_name",
            "protocol",
            "title",
            "images",
            "stylesheets_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_url(self, value):
        """Validate that the input is a valid URL."""
        if not validators.url(value):
            raise serializers.ValidationError("Invalid URL format.")
        return value
