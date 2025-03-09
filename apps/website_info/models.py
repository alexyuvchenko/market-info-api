from django.db import models


class WebsiteInfo(models.Model):
    """Model to store information about websites."""

    url = models.URLField(max_length=2000)
    domain_name = models.CharField(max_length=255)
    protocol = models.CharField(max_length=10)
    title = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list)
    stylesheets_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Website Information"
        verbose_name_plural = "Website Information"

    def __str__(self):
        return self.url
