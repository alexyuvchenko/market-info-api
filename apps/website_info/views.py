from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import WebsiteInfo
from .serializers import URLValidator, WebsiteInfoSerializer


class WebsiteInfoView(viewsets.ModelViewSet):
    """
    API endpoint for managing website information.

    Provides CRUD operations for website information:
    - List all website information
    - Create new website information by providing a URL
    - Retrieve specific website information by ID
    - Delete specific website information by ID
    """

    queryset = WebsiteInfo.objects.all()
    serializer_class = WebsiteInfoSerializer

    def list(self, request, *args, **kwargs):
        """
        List all website information entries.

        Returns a paginated list of all website information entries in the database.
        """

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific website information entry.

        Returns the details of a specific website information entry identified by its ID.
        """

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific website information entry.

        Permanently removes a website information entry from the database.
        """

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new website information entry.

        Fetches the provided URL, extracts information such as domain name, protocol,
        title, images, and stylesheets count, and stores it in the database.

        If the URL already exists in the database, returns the existing entry instead
        of creating a new one.

        Parameters:
        - url: The URL to fetch and extract information from

        Returns:
        - 201 Created: If a new entry was created
        - 200 OK: If the URL already exists
        - 400 Bad Request: If the URL is invalid or cannot be fetched
        - 500 Internal Server Error: If an error occurs during processing
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
            website_info = self._extract_website_info(url)

            # Create WebsiteInfo object
            serializer = self.get_serializer(data=website_info)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to fetch URL: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to process website: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _extract_website_info(self, url):
        """Extract information from the website."""

        # Parse URL
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        protocol = parsed_url.scheme

        # Fetch website content
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Return website info
        return {
            "url": url,
            "domain_name": domain_name,
            "protocol": protocol,
            "title": soup.title.text.strip() if soup.title else None,
            "images": self._extract_image_url(soup, protocol, domain_name),
            "stylesheets_count": len(soup.find_all("link", rel="stylesheet")),
        }

    def _extract_image_url(self, soup, protocol, domain_name):
        """Extract and normalize image URLs from the soup."""

        image_urls = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue

            # Normalize image URL
            if src.startswith("//"):
                src = f"{protocol}:{src}"
            elif src.startswith("/"):
                src = f"{protocol}://{domain_name}{src}"
            elif not src.startswith(("http://", "https://")):
                src = f"{protocol}://{domain_name}/{src}"

            image_urls.append(src)

        return image_urls
