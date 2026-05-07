# Permisos por rol y método para app_2_clinico_salud

from rest_framework import viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt

from .models import HistoriaClinicaUnificada, EventosIncidentes
from .serializers import (
    HistoriaClinicaUnificadaSerializerAdmin,
    HistoriaClinicaUnificadaSerializerEnfermeroJefe,
    HistoriaClinicaUnificadaSerializerTecnicoEnfermero,
    HistoriaClinicaUnificadaSerializerNutricionista,
    HistoriaClinicaUnificadaSerializerCocineros,
    HistoriaClinicaUnificadaSerializerMantenimiento,
    EventosIncidentesSerializer
)

ROLE_SERIALIZER_MAP_HISTORIA = {
    'administrador': HistoriaClinicaUnificadaSerializerAdmin,
    'enfermero jefe': HistoriaClinicaUnificadaSerializerEnfermeroJefe,
    'tecnico enfermero': HistoriaClinicaUnificadaSerializerTecnicoEnfermero,
    'nutricionista': HistoriaClinicaUnificadaSerializerNutricionista,
    'cocineros': HistoriaClinicaUnificadaSerializerCocineros,
    'mantenimiento': HistoriaClinicaUnificadaSerializerMantenimiento,
}

PUBLIC_KEY = settings.PUBLIC_KEY

USER_ID_CLAIMS = ('user_id', 'id_usuario', 'usuario_id', 'personal_id', 'id', 'uid', 'sub')



def get_role_from_jwt(request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise AuthenticationFailed('No se proporcionó token Bearer')
    token = auth.split(' ')[1]
    payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
    role = payload.get('role')
    if not role:
        
        raise AuthenticationFailed('El token no contiene rol')
    return role


def get_jwt_payload(request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise AuthenticationFailed('No se proporcionó token Bearer')
    token = auth.split(' ')[1]
    payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
    # print("PAYLOAD JWT RECIBIDO DEL FRONTEND:", payload)
    return payload


def get_user_id_from_jwt(request):
    payload = get_jwt_payload(request)

    for claim in USER_ID_CLAIMS:
        value = payload.get(claim)
        if value not in (None, ''):
            return str(value)

    raise AuthenticationFailed('El token no contiene un identificador de usuario válido')


class RolePermission(permissions.BasePermission):
    # Matriz de permisos por rol y método
    ROLE_METHODS = {
        'administrador': {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'},
        'enfermero jefe': {'GET', 'POST', 'PUT', 'PATCH'},
        'tecnico enfermero': {'GET', 'POST'},
        'nutricionista': {'GET'},
        'cocineros': set(),
        'mantenimiento': set(),
    }

    def has_permission(self, request, view):
        try:
            role = get_role_from_jwt(request)
            allowed_methods = self.ROLE_METHODS.get(role, set())
            print(f'[DEBUG] Método: {request.method}, Rol: {role}, Métodos permitidos: {allowed_methods}')
            # GET siempre permitido para todos los roles válidos con serializador
            if request.method == 'GET' and role in ROLE_SERIALIZER_MAP_HISTORIA:
                return True
            return request.method in allowed_methods
        except AuthenticationFailed as e:
            print(f'[DEBUG] Fallo de autenticación: {e}')
            return False






class PersonalFromJWTMixin:
    def perform_create(self, serializer):
        actor_id = get_user_id_from_jwt(self.request)
        serializer.save(creado_por=actor_id, actualizado_por=actor_id)

    def perform_update(self, serializer):
        serializer.save(actualizado_por=get_user_id_from_jwt(self.request))

class HistoriaClinicaUnificadaViewSet(PersonalFromJWTMixin, viewsets.ModelViewSet):

    queryset = HistoriaClinicaUnificada.objects.all()
    permission_classes = [RolePermission]

    def get_serializer_class(self):
        role = get_role_from_jwt(self.request)
        return ROLE_SERIALIZER_MAP_HISTORIA.get(role, HistoriaClinicaUnificadaSerializerAdmin)


class EventosIncidentesViewSet(PersonalFromJWTMixin, viewsets.ModelViewSet):
    queryset = EventosIncidentes.objects.all()
    serializer_class = EventosIncidentesSerializer
    permission_classes = [RolePermission]
