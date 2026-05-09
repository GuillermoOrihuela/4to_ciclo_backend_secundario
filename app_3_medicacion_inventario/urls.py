from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdministracionMedicacionViewSet,
    MedicacionPacienteViewSet,
    RecetasPacienteViewSet,
)

router = DefaultRouter()
router.register(r'recetas', RecetasPacienteViewSet, basename='recetas_paciente')
router.register(r'medicaciones', MedicacionPacienteViewSet, basename='medicacion_paciente')
router.register(r'administraciones', AdministracionMedicacionViewSet, basename='administracion_medicacion')

urlpatterns = [
    path('', include(router.urls)),
]
