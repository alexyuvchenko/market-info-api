from django.contrib import admin

from .models import WebsiteInfo


@admin.register(WebsiteInfo)
class WebsiteInfoAdmin(admin.ModelAdmin):
    """Admin configuration for the WebsiteInfo model."""

    list_display = ("url", "domain_name", "protocol", "stylesheets_count", "created_at")
    list_filter = ("protocol", "created_at")
    search_fields = ("url", "domain_name", "title")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("url", "domain_name", "protocol")}),
        ("Content Information", {"fields": ("title", "images", "stylesheets_count")}),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )
