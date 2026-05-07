from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HistoriaClinicaUnificadaViewSet,
    EventosIncidentesViewSet
)

router = DefaultRouter()
router.register(r'historias_clinicas', HistoriaClinicaUnificadaViewSet, basename='historias_clinicas')
router.register(r'eventos', EventosIncidentesViewSet, basename='eventos')

urlpatterns = [
    path('', include(router.urls)),
]
