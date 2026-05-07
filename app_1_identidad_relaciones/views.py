import jwt
from rest_framework import status
from rest_framework.response import Response
# Cargar la clave pública real desde el archivo
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import os

from .models import PacienteModel, FamiliarModel, RelacionPacienteFamiliarModel
from .serializers import (
	PacienteSerializerAdmin, PacienteSerializerEnfermeroJefe, 
	PacienteSerializerTecnicoEnfermero, PacienteSerializerNutricionista,
	FamiliarSerializerAdmin, FamiliarSerializerEnfermeroJefe, 
	FamiliarSerializerTecnicoEnfermero, FamiliarSerializerNutricionista,
	RelacionPacienteFamiliarSerializerAdmin, RelacionPacienteFamiliarSerializerEnfermeroJefe, 
	RelacionPacienteFamiliarSerializerTecnicoEnfermero, RelacionPacienteFamiliarSerializerNutricionista
)

ROLE_SERIALIZER_MAP_PACIENTE = {
	'administrador': PacienteSerializerAdmin,
	'enfermero jefe': PacienteSerializerEnfermeroJefe,
	'tecnico enfermero': PacienteSerializerTecnicoEnfermero,
	'nutricionista': PacienteSerializerNutricionista,
}

ROLE_SERIALIZER_MAP_FAMILIAR = {
	'administrador': FamiliarSerializerAdmin,
	'enfermero jefe': FamiliarSerializerEnfermeroJefe,
	'tecnico enfermero': FamiliarSerializerTecnicoEnfermero,
	'nutricionista': FamiliarSerializerNutricionista,
}

ROLE_SERIALIZER_MAP_RELACION = {
	'administrador': RelacionPacienteFamiliarSerializerAdmin,
	'enfermero jefe': RelacionPacienteFamiliarSerializerEnfermeroJefe,
	'tecnico enfermero': RelacionPacienteFamiliarSerializerTecnicoEnfermero,
	'nutricionista': RelacionPacienteFamiliarSerializerNutricionista,
}

# Usar la clave pública desde settings
from django.conf import settings
PUBLIC_KEY = settings.PUBLIC_KEY

def get_role_from_jwt(request):
	"""
	Extrae y valida el JWT del header Authorization y retorna el rol del usuario.
	"""
	auth = request.headers.get('Authorization')
	if not auth or not auth.startswith('Bearer '):
		print('[DEBUG] No se proporcionó token Bearer')
		raise AuthenticationFailed('No se proporcionó token Bearer')
	token = auth.split(' ')[1]
	try:
		payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
		role = payload.get('role')
		print(f'[DEBUG] JWT payload: {payload}')
		if not role:
			print('[DEBUG] El token no contiene rol')
			raise AuthenticationFailed('El token no contiene rol')
		print(f'[DEBUG] Rol extraído del JWT: {role}')
		return role
	except jwt.ExpiredSignatureError:
		print('[DEBUG] Token expirado')
		raise AuthenticationFailed('Token expirado')
	except jwt.InvalidTokenError as e:
		print(f'[DEBUG] Token inválido: {e}')
		raise AuthenticationFailed('Token inválido')

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
			if request.method == 'GET' and (role in ROLE_SERIALIZER_MAP_PACIENTE or role in ROLE_SERIALIZER_MAP_FAMILIAR):
				return True
			return request.method in allowed_methods
		except AuthenticationFailed as e:
			print(f'[DEBUG] Fallo de autenticación: {e}')
			return False





# ViewSet para RelacionPacienteFamiliar
class RelacionPacienteFamiliarViewSet(viewsets.ModelViewSet):
	queryset = RelacionPacienteFamiliarModel.objects.all()
	permission_classes = [RolePermission]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_RELACION.get(role, RelacionPacienteFamiliarSerializerAdmin)






# ViewSet para Paciente
class PacienteViewSet(viewsets.ModelViewSet):
	queryset = PacienteModel.objects.all()
	permission_classes = [RolePermission]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_PACIENTE.get(role, PacienteSerializerAdmin)

# ViewSet para Familiar


class FamiliarViewSet(viewsets.ModelViewSet):
	queryset = FamiliarModel.objects.all()
	permission_classes = [RolePermission]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_FAMILIAR.get(role, FamiliarSerializerAdmin)

	def dispatch(self, request, *args, **kwargs):
		role = get_role_from_jwt(request)
		if role != 'administrador':
			return Response({'detail': 'No tiene permiso para acceder a familiares.'}, status=status.HTTP_403_FORBIDDEN)
		return super().dispatch(request, *args, **kwargs)
