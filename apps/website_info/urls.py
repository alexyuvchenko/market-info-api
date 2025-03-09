from django.urls import re_path

from .views import WebsiteInfoView

urlpatterns = [
    # List and create
    re_path(
        r"^website-info/?$",
        WebsiteInfoView.as_view({"get": "list", "post": "create"}),
        name="websiteinfo-list",
    ),
    # Retrieve, update, and destroy
    re_path(
        r"^website-info/(?P<pk>[^/.]+)/?$",
        WebsiteInfoView.as_view({"get": "retrieve", "delete": "destroy"}),
        name="websiteinfo-detail",
    ),
]
