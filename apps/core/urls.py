from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WebsiteInfoViewSet

router = DefaultRouter()
router.register(r'websites', WebsiteInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
