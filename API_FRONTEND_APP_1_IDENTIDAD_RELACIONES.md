# API Frontend - App 1: Identidad y Relaciones

Esta app agrupa los recursos de identidad del paciente, familiares y sus relaciones.

Base URL:

```http
/api/
```

## Autenticación

Enviar siempre:

```http
Authorization: Bearer <jwt_personalizado>
```

Roles usados por esta app:

- administrador
- enfermero jefe
- tecnico enfermero
- nutricionista

## Permisos por rol

### Pacientes

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

### Familiares

- Todos los métodos: solo administrador

### Relaciones paciente-familiar

- GET: administrador, enfermero jefe, tecnico enfermero, nutricionista
- POST: administrador, enfermero jefe, tecnico enfermero
- PUT/PATCH: administrador, enfermero jefe
- DELETE: administrador

## 1. Pacientes

### Endpoint

```http
/api/pacientes/
```

### Crear paciente

```http
POST /api/pacientes/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "dni": "12345678",
  "nombres": "Juan",
  "apellidos": "Pérez",
  "fecha_nacimiento": "1980-05-10",
  "sexo": "M",
  "direccion": "Av. Siempre Viva 123",
  "distrito": "Lima",
  "ciudad": "Lima",
  "estado_civil": "CASADO",
  "estado_paciente": "ACTIVO"
}
```

Opciones para `sexo`:

- M
- F

Opciones para `estado_civil`:

- SOLTERO
- SOLTERA
- CASADO
- CASADA
- DIVORCIADO
- DIVORCIADA
- VIUDO
- VIUDA

Opciones para `estado_paciente`:

- REGISTRADO
- ACTIVO
- HOSPITALIZADO
- EN_TRATAMIENTO
- ALTA_MEDICA
- REFERIDO
- FALLECIDO
- INACTIVO

### Actualizar paciente

```http
PUT /api/pacientes/1/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "dni": "12345678",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez",
  "fecha_nacimiento": "1980-05-10",
  "sexo": "M",
  "direccion": "Av. Siempre Viva 123",
  "distrito": "Lima",
  "ciudad": "Lima",
  "estado_civil": "CASADO",
  "estado_paciente": "ACTIVO"
}
```

### Respuesta ejemplo

```json
[
  {
    "id_paciente": 1,
    "dni": "12345678",
    "nombres": "Juan",
    "apellidos": "Pérez",
    "fecha_nacimiento": "1980-05-10",
    "sexo": "M",
    "direccion": "Av. Siempre Viva 123",
    "distrito": "Lima",
    "ciudad": "Lima",
    "estado_civil": "CASADO",
    "estado_paciente": "ACTIVO",
    "fecha_creacion": "2024-03-29T12:00:00Z",
    "fecha_modificacion": "2024-03-29T12:00:00Z"
  }
]
```

### Endpoints disponibles

- GET `/api/pacientes/`
- POST `/api/pacientes/`
- GET `/api/pacientes/{id}/`
- PUT/PATCH `/api/pacientes/{id}/`
- DELETE `/api/pacientes/{id}/`

## 2. Familiares

### Endpoint

```http
/api/familiares/
```

### Crear familiar

```http
POST /api/familiares/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "dni": "11223344",
  "nombres": "Ana",
  "apellidos": "García",
  "movil": "987654321",
  "sexo": "F",
  "direccion": "Calle Falsa 456",
  "distrito": "Miraflores",
  "ciudad": "Lima"
}
```

### Actualizar familiar

```http
PUT /api/familiares/1/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "dni": "11223344",
  "nombres": "Ana María",
  "apellidos": "García",
  "movil": "987654321",
  "sexo": "F",
  "direccion": "Calle Falsa 456",
  "distrito": "Miraflores",
  "ciudad": "Lima"
}
```

### Endpoints disponibles

- GET `/api/familiares/`
- POST `/api/familiares/`
- GET `/api/familiares/{id}/`
- PUT/PATCH `/api/familiares/{id}/`
- DELETE `/api/familiares/{id}/`

Nota:

- El acceso a familiares está restringido a `administrador`.

## 3. Relaciones Paciente-Familiar

### Endpoint

```http
/api/relaciones/
```

### Crear relación

```http
POST /api/relaciones/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "id_familiar": 1,
  "parentesco": "PADRE",
  "es_responsable_emergencia": "SI"
}
```

Opciones para `parentesco`:

- PADRE
- MADRE
- HIJO
- HIJA
- CONYUGE
- HERMANO
- HERMANA
- ABUELO
- ABUELA
- NIETO
- NIETA
- TIO
- TIA
- SOBRINO
- SOBRINA
- PRIMO
- PRIMA
- OTRO

Opciones para `es_responsable_emergencia`:

- SI
- NO

### Actualizar relación

```http
PUT /api/relaciones/1/ HTTP/1.1
Host: <host>
Authorization: Bearer <jwt_personalizado>
Content-Type: application/json

{
  "id_paciente": 1,
  "id_familiar": 2,
  "parentesco": "CONYUGE",
  "es_responsable_emergencia": "NO"
}
```

### Respuesta ejemplo

```json
[
  {
    "id_relacion": 1,
    "id_paciente": 1,
    "id_familiar": 1,
    "parentesco": "PADRE",
    "es_responsable_emergencia": "SI",
    "fecha_creacion": "2024-03-29T12:00:00Z",
    "fecha_modificacion": "2024-03-29T12:00:00Z"
  }
]
```

### Endpoints disponibles

- GET `/api/relaciones/`
- POST `/api/relaciones/`
- GET `/api/relaciones/{id}/`
- PUT/PATCH `/api/relaciones/{id}/`
- DELETE `/api/relaciones/{id}/`

## 4. Ejemplo de envío del JWT desde frontend

### fetch

```js
fetch('http://localhost:8000/api/pacientes/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer TU_TOKEN_JWT',
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### axios

```js
import axios from 'axios';

axios.get('http://localhost:8000/api/pacientes/', {
  headers: {
    'Authorization': 'Bearer TU_TOKEN_JWT'
  }
})
  .then(response => {
    console.log(response.data);
  });
```

## 5. Notas

- Los IDs enviados en relaciones deben existir previamente.
- Los campos visibles y editables cambian según el rol contenido en el JWT.
- Si el rol no tiene permiso para el endpoint, la API responde 403.