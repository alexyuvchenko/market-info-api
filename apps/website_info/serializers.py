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
    """Serializer for the WebsiteInfo model."""

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
