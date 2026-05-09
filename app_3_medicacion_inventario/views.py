import jwt
from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.exceptions import AuthenticationFailed

from .models import AdministracionMedicacion, MedicacionPaciente, RecetasPaciente
from .serializers import (
	AdministracionMedicacionSerializerAdmin,
	AdministracionMedicacionSerializerEnfermeroJefe,
	AdministracionMedicacionSerializerNutricionista,
	AdministracionMedicacionSerializerTecnicoEnfermero,
	MedicacionPacienteSerializerAdmin,
	MedicacionPacienteSerializerEnfermeroJefe,
	MedicacionPacienteSerializerNutricionista,
	MedicacionPacienteSerializerTecnicoEnfermero,
	RecetasPacienteSerializerAdmin,
	RecetasPacienteSerializerEnfermeroJefe,
	RecetasPacienteSerializerNutricionista,
	RecetasPacienteSerializerTecnicoEnfermero,
)


PUBLIC_KEY = settings.PUBLIC_KEY


ROLE_SERIALIZER_MAP_RECETAS = {
	'administrador': RecetasPacienteSerializerAdmin,
	'enfermero jefe': RecetasPacienteSerializerEnfermeroJefe,
	'tecnico enfermero': RecetasPacienteSerializerTecnicoEnfermero,
	'nutricionista': RecetasPacienteSerializerNutricionista,
}

ROLE_SERIALIZER_MAP_MEDICACION = {
	'administrador': MedicacionPacienteSerializerAdmin,
	'enfermero jefe': MedicacionPacienteSerializerEnfermeroJefe,
	'tecnico enfermero': MedicacionPacienteSerializerTecnicoEnfermero,
	'nutricionista': MedicacionPacienteSerializerNutricionista,
}

ROLE_SERIALIZER_MAP_ADMINISTRACION = {
	'administrador': AdministracionMedicacionSerializerAdmin,
	'enfermero jefe': AdministracionMedicacionSerializerEnfermeroJefe,
	'tecnico enfermero': AdministracionMedicacionSerializerTecnicoEnfermero,
	'nutricionista': AdministracionMedicacionSerializerNutricionista,
}


def get_role_from_jwt(request):
	auth = request.headers.get('Authorization')
	if not auth or not auth.startswith('Bearer '):
		raise AuthenticationFailed('No se proporciono token Bearer')

	token = auth.split(' ')[1]
	try:
		payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
	except jwt.ExpiredSignatureError:
		raise AuthenticationFailed('Token expirado')
	except jwt.InvalidTokenError:
		raise AuthenticationFailed('Token invalido')

	role = payload.get('role')
	if not role:
		raise AuthenticationFailed('El token no contiene rol')

	return role


class RolePermissionRecetas(permissions.BasePermission):
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
			if request.method == 'GET' and role in ROLE_SERIALIZER_MAP_RECETAS:
				return True
			return request.method in self.ROLE_METHODS.get(role, set())
		except AuthenticationFailed:
			return False


class RolePermissionMedicacion(permissions.BasePermission):
	ROLE_METHODS = {
		'administrador': {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'},
		'enfermero jefe': {'GET', 'POST', 'PUT', 'PATCH'},
		'tecnico enfermero': {'GET', 'POST', 'PUT', 'PATCH'},
		'nutricionista': {'GET'},
		'cocineros': set(),
		'mantenimiento': set(),
	}

	def has_permission(self, request, view):
		try:
			role = get_role_from_jwt(request)
			if request.method == 'GET' and role in ROLE_SERIALIZER_MAP_MEDICACION:
				return True
			return request.method in self.ROLE_METHODS.get(role, set())
		except AuthenticationFailed:
			return False


class RolePermissionAdministracion(permissions.BasePermission):
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
			if request.method == 'GET' and role in ROLE_SERIALIZER_MAP_ADMINISTRACION:
				return True
			return request.method in self.ROLE_METHODS.get(role, set())
		except AuthenticationFailed:
			return False


class RecetasPacienteViewSet(viewsets.ModelViewSet):
	queryset = RecetasPaciente.objects.all()
	permission_classes = [RolePermissionRecetas]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_RECETAS.get(role, RecetasPacienteSerializerAdmin)


class MedicacionPacienteViewSet(viewsets.ModelViewSet):
	queryset = MedicacionPaciente.objects.all()
	permission_classes = [RolePermissionMedicacion]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_MEDICACION.get(role, MedicacionPacienteSerializerAdmin)


class AdministracionMedicacionViewSet(viewsets.ModelViewSet):
	queryset = AdministracionMedicacion.objects.all()
	permission_classes = [RolePermissionAdministracion]

	def get_serializer_class(self):
		role = get_role_from_jwt(self.request)
		return ROLE_SERIALIZER_MAP_ADMINISTRACION.get(role, AdministracionMedicacionSerializerAdmin)
