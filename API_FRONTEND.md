# Integración Frontend por Apps

La documentación de integración para frontend fue separada por aplicación para que cada módulo tenga sus propios endpoints, permisos y ejemplos.

## Documentos disponibles

### App 1: Identidad y relaciones

Incluye los endpoints de:

- Pacientes
- Familiares
- Relaciones paciente-familiar

Archivo: `API_FRONTEND_APP_1_IDENTIDAD_RELACIONES.md`

### App 2: Clínico y salud

Incluye los endpoints de:

- Historias clínicas unificadas
- Seguimientos diarios
- Eventos e incidentes

Archivo: `API_FRONTEND_APP_2_CLINICO_SALUD.md`

## Autenticación común

Ambas apps esperan un JWT emitido por el backend principal en la cabecera:

```http
Authorization: Bearer <jwt_personalizado>
```

Payload esperado del token:

```json
{
  "role": "<rol_usuario>",
  "iat": 1711756800,
  "exp": 1711792800
}
```

Notas:

- El frontend no debe modificar el JWT.
- Si el token es inválido, expiró o no fue enviado, la API responde 401 o 403 según el caso.
- La app 1 se expone bajo `/api/`.
- La app 2 se expone bajo `/api/clinico/`.

## Resumen de permisos

### App 1: Identidad y relaciones

#### Pacientes

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

#### Familiares

- GET, POST, PUT, PATCH, DELETE: administrador

#### Relaciones paciente-familiar

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

### App 2: Clínico y salud

#### Historias clínicas

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista, cocineros, mantenimiento
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero, nutricionista
- DELETE: administrador

#### Seguimientos

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero
- DELETE: administrador

#### Eventos e incidentes

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero
- DELETE: administrador