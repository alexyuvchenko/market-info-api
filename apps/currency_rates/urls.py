from django.urls import re_path

from .views import CurrencyRatesView

urlpatterns = [
    re_path(r"^currency-rates/?$", CurrencyRatesView.as_view(), name="currency-rates"),
]
