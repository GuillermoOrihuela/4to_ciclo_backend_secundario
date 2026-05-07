# API Frontend - App 2: Clínico y Salud

Esta app concentra la información clínica del paciente y se expone bajo el prefijo clínico.

Base URL:

```http
/api/clinico/
```

## Autenticación

Enviar siempre:

```http
Authorization: Bearer <jwt_personalizado>
```

El backend toma el rol desde el JWT y también extrae automáticamente el id del usuario para registrar quién crea o modifica cada registro.

## Campos de auditoría

Esta app registra automáticamente quién crea y quién actualiza cada registro.

- `creado_por`: se asigna al crear el registro con el id extraído del JWT. El frontend **no lo envía**.
- `actualizado_por`: se actualiza en cada PUT/PATCH con el id del usuario del JWT. El frontend **no lo envía**.

Ambos campos son de **solo lectura** desde la API. Si el frontend los envía, son ignorados.

El backend busca el id del usuario en el payload JWT usando estos claims en orden:

- `user_id`
- `id_usuario`
- `usuario_id`
- `personal_id`
- `id`
- `uid`
- `sub`

Si el payload no contiene ninguno, el backend responde 403.

Ejemplo de payload JWT válido:

```json
{
  "user_id": "42",
  "role": "enfermero jefe",
  "iat": 1711756800,
  "exp": 1711792800
}
```

## Permisos reales por método

La app 2 ahora usa permisos por rol y por método en cada recurso.

### Historias clínicas

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista, cocineros, mantenimiento
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero, nutricionista
- DELETE: administrador


### Eventos e incidentes

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero
- DELETE: administrador

## 1. Historias clínicas unificadas

### Endpoint

```http
/api/clinico/historias_clinicas/
```

### Endpoints disponibles

- GET `/api/clinico/historias_clinicas/`
- POST `/api/clinico/historias_clinicas/`
- GET `/api/clinico/historias_clinicas/{id}/`
- PUT/PATCH `/api/clinico/historias_clinicas/{id}/`
- DELETE `/api/clinico/historias_clinicas/{id}/`

### Acceso por rol

- administrador: acceso completo
- enfermero jefe: GET, POST, PUT, PATCH
- tecnico enfermero: GET, POST, PUT, PATCH
- nutricionista: GET, PUT, PATCH
- cocineros: GET
- mantenimiento: GET

Nota:

- La respuesta cambia según el serializer asignado por rol.

### Crear historia clínica

```http
POST /api/clinico/historias_clinicas/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "motivo_ingreso": "Dolor abdominal persistente",
  "diagnostico_inicial": "Gastritis aguda",
  "alergias": "Penicilina",
  "tratamiento_actual": "Observación y medicación",
  "nutricion_asignada": "Dieta blanda"
}
```

Campos que **no debes enviar** (el backend los completa desde el JWT):

- `creado_por`
- `actualizado_por`

### Respuesta ejemplo (rol: administrador)

```json
{
  "id_historia": 1,
  "id_paciente": 1,
  "motivo_ingreso": "Dolor abdominal persistente",
  "diagnostico_inicial": "Gastritis aguda",
  "alergias": "Penicilina",
  "tratamiento_actual": "Observación y medicación",
  "nutricion_asignada": "Dieta blanda",
  "creado_por": "42",
  "actualizado_por": "42"
}
```

### Visibilidad por rol

- administrador: ve todos los campos
- enfermero jefe: igual que administrador
- tecnico enfermero: no ve `nutricion_asignada`
- nutricionista: no ve `diagnostico_inicial` ni `tratamiento_actual`
- cocineros: solo ve `id_historia`, `id_paciente`, `nutricion_asignada`
- mantenimiento: solo ve `id_historia`, `id_paciente`


## 3. Eventos e incidentes

### Endpoint

```http
/api/clinico/eventos/
```

### Endpoints disponibles

- GET `/api/clinico/eventos/`
- POST `/api/clinico/eventos/`
- GET `/api/clinico/eventos/{id}/`
- PUT/PATCH `/api/clinico/eventos/{id}/`
- DELETE `/api/clinico/eventos/{id}/`

### Acceso por rol

- administrador: GET, POST, PUT, PATCH, DELETE
- enfermero jefe: GET, POST, PUT, PATCH
- tecnico enfermero: GET, POST, PUT, PATCH
- nutricionista: GET

Nota:

- En este recurso no hay serializer distinto por rol en la implementación actual.

### Crear evento o incidente

```http
POST /api/clinico/eventos/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "tipo_evento": "Caída",
  "descripcion": "Paciente sufrió una caída al trasladarse al baño",
  "acciones_tomadas": "Se evaluó al paciente y se notificó al responsable",
  "gravedad": "Media",
  "fecha_evento": "2026-04-11",
  "hora_evento": "08:45:00"
}
```

Campos que **no debes enviar** (el backend los completa desde el JWT):

- `creado_por`
- `actualizado_por`

Opciones para `tipo_evento`:

- Caída
- Emergencia Médica
- Conflicto
- Otro

Opciones para `gravedad`:

- Baja
- Media
- Alta

### Respuesta ejemplo

```json
{
  "id_evento": 1,
  "id_paciente": 1,
  "creado_por": "42",
  "actualizado_por": "42",
  "tipo_evento": "Caída",
  "descripcion": "Paciente sufrió una caída al trasladarse al baño",
  "acciones_tomadas": "Se evaluó al paciente y se notificó al responsable",
  "gravedad": "Media",
  "fecha_evento": "2026-04-11",
  "hora_evento": "08:45:00"
}
```

## 4. Notas de integración

- Todos los viewsets de esta app requieren autenticación.
- El backend valida el JWT con la clave pública configurada en el proyecto.
- Si el token no contiene rol, la petición falla.
- Si el token no contiene un identificador de usuario válido para crear o actualizar, la operación falla.
- `id_paciente` debe existir previamente en la app 1.
- Los permisos por rol se aplican en los viewsets de historias clínicas, seguimientos y eventos.

