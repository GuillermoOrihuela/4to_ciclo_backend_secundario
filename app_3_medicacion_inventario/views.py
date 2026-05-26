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
USER_ID_CLAIMS = ('user_id', 'id_usuario', 'usuario_id', 'personal_id', 'id', 'uid', 'sub')
NAME_CLAIMS = (
	'full_name',
	'nombre_completo',
	'display_name',
	'name',
	'username',
	'preferred_username',
	'email',
)
FIRST_NAME_CLAIMS = ('nombres', 'nombre', 'first_name', 'given_name')
LAST_NAME_CLAIMS = ('apellidos', 'apellido', 'last_name', 'family_name')


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


def get_jwt_payload(request):
	auth = request.headers.get('Authorization')
	if not auth or not auth.startswith('Bearer '):
		raise AuthenticationFailed('No se proporciono token Bearer')

	token = auth.split(' ')[1]
	try:
		return jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
	except jwt.ExpiredSignatureError:
		raise AuthenticationFailed('Token expirado')
	except jwt.InvalidTokenError:
		raise AuthenticationFailed('Token invalido')


def get_user_id_from_jwt(request):
	payload = get_jwt_payload(request)

	for claim in USER_ID_CLAIMS:
		value = payload.get(claim)
		if value in (None, ''):
			continue
		try:
			return int(value)
		except (TypeError, ValueError):
			raise AuthenticationFailed('El token contiene un identificador de usuario invalido')

	raise AuthenticationFailed('El token no contiene un identificador de usuario valido')


def get_user_name_from_jwt(request):
	payload = get_jwt_payload(request)

	for claim in NAME_CLAIMS:
		value = payload.get(claim)
		if isinstance(value, str) and value.strip():
			return value.strip()

	first_name = ''
	last_name = ''
	for claim in FIRST_NAME_CLAIMS:
		value = payload.get(claim)
		if isinstance(value, str) and value.strip():
			first_name = value.strip()
			break

	for claim in LAST_NAME_CLAIMS:
		value = payload.get(claim)
		if isinstance(value, str) and value.strip():
			last_name = value.strip()
			break

	full_name = f'{first_name} {last_name}'.strip()
	if full_name:
		return full_name

	return None


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

	def perform_create(self, serializer):
		user_id = get_user_id_from_jwt(self.request)
		nombre_personal_entrega = serializer.validated_data.get('nombre_personal_entrega') or get_user_name_from_jwt(self.request)
		serializer.save(
			id_personal_entrega=str(user_id),
			nombre_personal_entrega=nombre_personal_entrega,
		)
