from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import LetterViewSet

app_name = 'outbox'

router = DefaultRouter()
router.register(r'letters', LetterViewSet, basename='letter')

urlpatterns = [
    path('api/', include(router.urls)),
]