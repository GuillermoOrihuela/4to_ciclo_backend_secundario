Actualiza el frontend del modulo Clinico/Salud para alinearlo con el backend actual.

Contexto del cambio:

- El recurso HistoriaClinicaUnificada ya no maneja el campo motivo_ingreso.
- El backend dejo de aceptar motivo_ingreso en create/update.
- El backend ya no devuelve motivo_ingreso en list/detail.

Objetivo:

- Eliminar motivo_ingreso de toda la UI, estado, validaciones, requests y mapeos relacionados con HistoriaClinicaUnificada.

Cambios requeridos:

1. Formularios de crear y editar historia clinica:
- Quitar el input, textarea o control asociado a motivo_ingreso.
- Ajustar validaciones para que no lo exijan ni lo consideren.
- Revisar textos, labels y mensajes de error para que no lo mencionen.

2. Requests al backend:
- Dejar de enviar motivo_ingreso en POST, PUT y PATCH de historias clinicas.
- Si existe un builder, mapper o normalizador de payload, eliminar esa propiedad.

3. Lectura de respuestas:
- Quitar motivo_ingreso de interfaces, types, schemas, DTOs o modelos de frontend.
- Eliminar su uso en tablas, cards, modales, vistas detalle y resúmenes.
- Evitar fallos por destructuring o renderizado de una propiedad inexistente.

4. Estado y cache:
- Limpiar valores iniciales, estados locales, reducers, stores o cache keys que incluyan motivo_ingreso.

5. Pruebas:
- Actualizar tests unitarios, snapshots, mocks y fixtures para quitar motivo_ingreso.

6. Criterios de aceptacion:
- No aparece motivo_ingreso en ninguna pantalla de HistoriaClinicaUnificada.
- No se envia motivo_ingreso al backend.
- No hay errores de tipado, render o validacion por la eliminacion del campo.
- Crear/editar/listar/ver detalle sigue funcionando con los campos restantes.

Payload vigente de ejemplo para crear o actualizar:

```json
{
  "id_paciente": 1,
  "diagnostico_inicial": "Gastritis aguda",
  "alergias": "Penicilina",
  "tratamiento_actual": "Observacion y medicacion",
  "nutricion_asignada": "Dieta blanda"
}
```

Respuesta esperada de ejemplo:

```json
{
  "id_historia": 1,
  "id_paciente": 1,
  "diagnostico_inicial": "Gastritis aguda",
  "alergias": "Penicilina",
  "tratamiento_actual": "Observacion y medicacion",
  "nutricion_asignada": "Dieta blanda",
  "creado_por": "42",
  "actualizado_por": "42"
}
```