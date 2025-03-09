from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.website_info.urls")),
    path("api/", include("apps.currency_rates.urls")),
    # API Schema documentation - using regex to support both with and without trailing slash
    re_path(r"^api/schema/?$", SpectacularAPIView.as_view(), name="schema"),
    re_path(
        r"^api/schema/swagger-ui/?$",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    re_path(r"^api/schema/redoc/?$", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
