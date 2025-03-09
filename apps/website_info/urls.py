from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WebsiteInfoView

router = DefaultRouter()
router.register(r'website-info', WebsiteInfoView, basename='websiteinfo')

urlpatterns = [
    path('', include(router.urls)),
] 
