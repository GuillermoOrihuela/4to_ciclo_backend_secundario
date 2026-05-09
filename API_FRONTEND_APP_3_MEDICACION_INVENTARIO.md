# API Frontend - App 3: Medicación e Inventario

Este documento describe la implementación real disponible en backend para el módulo 3.

Lógica central:

- Cada paciente maneja sus propios medicamentos.
- El inventario está integrado en la medicación del paciente.
- No hay stock global compartido entre pacientes.

Base URL activa:

```http
/api/medicacion/
```

## Autenticación

Enviar siempre:

```http
Authorization: Bearer <jwt_personalizado>
```

El backend valida JWT RS256 y toma el rol desde el claim `role`.

## Roles usados

- administrador
- enfermero jefe
- tecnico enfermero
- nutricionista

## Permisos por rol y método

### 1) Recetas (`/api/medicacion/recetas/`)

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

### 2) Medicaciones (`/api/medicacion/medicaciones/`)

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe, tecnico enfermero
- DELETE: administrador

### 3) Administraciones (`/api/medicacion/administraciones/`)

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

## Modelos y campos

## 1. RecetasPaciente

Campos:

- `id_receta`
- `id_paciente`
- `medico_prescriptor`
- `fecha_prescripcion`
- `fecha_vencimiento`
- `diagnostico_receta`
- `estado`: `Activa`, `Vencida`, `Suspendida`

Endpoints disponibles:

- GET `/api/medicacion/recetas/`
- POST `/api/medicacion/recetas/`
- GET `/api/medicacion/recetas/{id}/`
- PUT/PATCH `/api/medicacion/recetas/{id}/`
- DELETE `/api/medicacion/recetas/{id}/`

Ejemplo crear receta:

```http
POST /api/medicacion/recetas/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "medico_prescriptor": "Dr. Herrera",
  "fecha_prescripcion": "2026-05-09",
  "fecha_vencimiento": "2026-06-09",
  "diagnostico_receta": "Hipertension arterial",
  "estado": "Activa"
}
```

Ejemplo respuesta:

```json
{
  "id_receta": 1,
  "id_paciente": 1,
  "medico_prescriptor": "Dr. Herrera",
  "fecha_prescripcion": "2026-05-09",
  "fecha_vencimiento": "2026-06-09",
  "diagnostico_receta": "Hipertension arterial",
  "estado": "Activa"
}
```

Visibilidad por rol (serializer):

- administrador: todos los campos
- enfermero jefe: todos los campos
- tecnico enfermero: todos los campos funcionales
- nutricionista: `id_receta`, `id_paciente`, `diagnostico_receta`, `estado` (solo lectura)

## 2. MedicacionPaciente

Campos:

- `id_medicacion`
- `id_paciente`
- `id_receta` (opcional)
- `nombre_medicamento`
- `tipo`: `Pastilla`, `Jarabe`, `Inyectable`, `Crema`
- `dosis`
- `frecuencia`
- `via_administracion`: `Oral`, `Topica`, `IV`
- `horarios_aplicacion`
- `duracion_dias`
- `cantidad_disponible`
- `unidad_medida`
- `proveedor_o_familiar`
- `fecha_ingreso`
- `fecha_vencimiento` (opcional)
- `lote` (opcional)
- `observaciones` (opcional)

Endpoints disponibles:

- GET `/api/medicacion/medicaciones/`
- POST `/api/medicacion/medicaciones/`
- GET `/api/medicacion/medicaciones/{id}/`
- PUT/PATCH `/api/medicacion/medicaciones/{id}/`
- DELETE `/api/medicacion/medicaciones/{id}/`

Ejemplo crear medicación de paciente:

```http
POST /api/medicacion/medicaciones/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "id_receta": 1,
  "nombre_medicamento": "Paracetamol 500mg",
  "tipo": "Pastilla",
  "dosis": "1 tableta",
  "frecuencia": "Cada 8 horas",
  "via_administracion": "Oral",
  "horarios_aplicacion": "06:00, 14:00, 22:00",
  "duracion_dias": 7,
  "cantidad_disponible": "50.00",
  "unidad_medida": "tableta",
  "proveedor_o_familiar": "Hijo del paciente",
  "fecha_ingreso": "2026-05-09",
  "fecha_vencimiento": "2027-02-01",
  "lote": "L-001-ABC",
  "observaciones": "Mantener en lugar seco"
}
```

Ejemplo respuesta:

```json
{
  "id_medicacion": 1,
  "id_paciente": 1,
  "id_receta": 1,
  "nombre_medicamento": "Paracetamol 500mg",
  "tipo": "Pastilla",
  "dosis": "1 tableta",
  "frecuencia": "Cada 8 horas",
  "via_administracion": "Oral",
  "horarios_aplicacion": "06:00, 14:00, 22:00",
  "duracion_dias": 7,
  "cantidad_disponible": "50.00",
  "unidad_medida": "tableta",
  "proveedor_o_familiar": "Hijo del paciente",
  "fecha_ingreso": "2026-05-09",
  "fecha_vencimiento": "2027-02-01",
  "lote": "L-001-ABC",
  "observaciones": "Mantener en lugar seco"
}
```

Visibilidad por rol (serializer):

- administrador: todos los campos
- enfermero jefe: todos los campos
- tecnico enfermero: campos clínicos + stock operativo
- nutricionista: `id_medicacion`, `id_paciente`, `nombre_medicamento`, `dosis`, `frecuencia`, `via_administracion`, `horarios_aplicacion` (solo lectura)

## 3. AdministracionMedicacion

Campos:

- `id_admin`
- `id_medicacion`
- `id_personal_entrega` (opcional)
- `fecha_hora_programada`
- `fecha_hora_real` (opcional)
- `cantidad_administrada`
- `estado`: `Entregado`, `Rechazado`, `Omitido`
- `motivo_rechazo` (opcional)

Endpoints disponibles:

- GET `/api/medicacion/administraciones/`
- POST `/api/medicacion/administraciones/`
- GET `/api/medicacion/administraciones/{id}/`
- PUT/PATCH `/api/medicacion/administraciones/{id}/`
- DELETE `/api/medicacion/administraciones/{id}/`

Ejemplo registrar administración:

```http
POST /api/medicacion/administraciones/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_medicacion": 1,
  "id_personal_entrega": 3,
  "fecha_hora_programada": "2026-05-09T14:00:00Z",
  "fecha_hora_real": "2026-05-09T14:02:00Z",
  "cantidad_administrada": "1.00",
  "estado": "Entregado",
  "motivo_rechazo": ""
}
```

Ejemplo respuesta:

```json
{
  "id_admin": 10,
  "id_medicacion": 1,
  "id_personal_entrega": 3,
  "fecha_hora_programada": "2026-05-09T14:00:00Z",
  "fecha_hora_real": "2026-05-09T14:02:00Z",
  "cantidad_administrada": "1.00",
  "estado": "Entregado",
  "motivo_rechazo": ""
}
```

Visibilidad por rol (serializer):

- administrador: todos los campos
- enfermero jefe: todos los campos
- tecnico enfermero: todos los campos operativos
- nutricionista: `id_admin`, `id_medicacion`, `fecha_hora_programada`, `estado` (solo lectura)

## Reglas recomendadas para frontend

- Filtrar siempre por paciente en recetas, medicaciones y administraciones.
- No mezclar datos de distintos pacientes en una misma vista de trabajo clínico.
- Si `estado = Rechazado`, solicitar `motivo_rechazo` obligatorio.
- Si `estado = Entregado`, solicitar `fecha_hora_real`.
- Alertar si `cantidad_administrada` es mayor a `cantidad_disponible`.
- Alertar si la medicación está vencida (`fecha_vencimiento` menor a fecha actual).

## Ejemplo de servicios frontend (TypeScript)

```ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/medicacion/',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const listarRecetas = () => api.get('recetas/');
export const crearReceta = (payload: any) => api.post('recetas/', payload);

export const listarMedicaciones = () => api.get('medicaciones/');
export const crearMedicacion = (payload: any) => api.post('medicaciones/', payload);

export const listarAdministraciones = () => api.get('administraciones/');
export const crearAdministracion = (payload: any) => api.post('administraciones/', payload);
```

## Checklist de integración

- Consumir rutas bajo `/api/medicacion/`.
- Enviar JWT en header Authorization.
- Implementar guardas de UI por rol para mostrar acciones permitidas.
- Implementar filtros por paciente en frontend.
- Manejar respuestas 401/403 por token inválido o rol sin permiso.
- Validar reglas clínicas antes de enviar POST/PUT/PATCH.

## Estado actual backend

- Modelos implementados
- Serializers implementados por rol
- Viewsets implementados con permisos por rol y método
- URLs de app implementadas
- Integración de app en configuración principal lista

Pendiente operativo:

- Ejecutar migraciones si aún no se ejecutaron (`makemigrations` y `migrate`)
