from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import WebsiteInfo
from .serializers import URLValidator, WebsiteInfoSerializer


class WebsiteInfoView(viewsets.ModelViewSet):
    """View for the WebsiteInfo model."""

    queryset = WebsiteInfo.objects.all()
    serializer_class = WebsiteInfoSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle URL validation and website information extraction.
        If the URL already exists, return the existing record instead of creating a new one.
        """
        # Validate URL
        url_validator = URLValidator(data=request.data)
        if not url_validator.is_valid():
            return Response(url_validator.errors, status=status.HTTP_400_BAD_REQUEST)

        url = url_validator.validated_data["url"]

        # Check if URL already exists
        existing_info = WebsiteInfo.objects.filter(url=url).first()
        if existing_info:
            serializer = self.get_serializer(existing_info)
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            # Extract website information
            website_info = self._extract_website_info(url)

            # Create WebsiteInfo object
            serializer = self.get_serializer(data={"url": url, **website_info})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to fetch URL: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _extract_website_info(self, url):
        """
        Extract information from the website.

        Args:
            url (str): The URL to extract information from.

        Returns:
            dict: Dictionary containing website information.
        """
        # Parse URL
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        protocol = parsed_url.scheme

        # Fetch website content
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.title.text if soup.title else None

        # Extract images
        images = [img.get("src") for img in soup.find_all("img") if img.get("src")]

        # Count stylesheets
        stylesheets_count = len(soup.find_all("link", rel="stylesheet"))

        return {
            "domain_name": domain_name,
            "protocol": protocol,
            "title": title,
            "images": images,
            "stylesheets_count": stylesheets_count,
        }
