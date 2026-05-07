from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, FamiliarViewSet, RelacionPacienteFamiliarViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'familiares', FamiliarViewSet, basename='familiar')
router.register(r'relaciones', RelacionPacienteFamiliarViewSet, basename='relacion')

urlpatterns = [
    path('', include(router.urls)),
]