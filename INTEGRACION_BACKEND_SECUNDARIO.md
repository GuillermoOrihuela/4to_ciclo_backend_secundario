# Instrucciones para integración con backend secundario

Este archivo describe cómo debe integrarse el backend secundario con el backend principal de usuarios, utilizando el nuevo payload JWT basado en roles.

---

## 1. Recepción del JWT

El backend secundario recibirá un JWT firmado (algoritmo RS256) en el header `Authorization`:

```
Authorization: Bearer <jwt_personalizado>
```

El payload del JWT tiene la siguiente estructura:

```json
{
  "role": "<rol_usuario>",
  "iat": 1711756800,
  "exp": 1711792800
}
```
- `role`: Rol del usuario autenticado (ej: "administrador", "enfermero jefe", etc.)
- `iat`: Timestamp de emisión
- `exp`: Timestamp de expiración

---

## 2. Validación del JWT

- Validar la firma con la clave pública correspondiente (algoritmo RS256).
- Verificar que el token no esté expirado (`exp`).
- Extraer el campo `role` del payload.

---

## 3. Control de acceso por rol

El backend secundario debe definir su propia matriz de permisos según el valor de `role` recibido. Ejemplo:

| Rol                | Permisos en backend secundario           |
|--------------------|-----------------------------------------|
| administrador      | Acceso total                            |
| enfermero jefe     | Acceso a endpoints de enfermería        |
| tecnico enfermero  | Acceso a endpoints de enfermería        |
| nutricionista      | Acceso a endpoints de nutrición         |
| cocineros          | Acceso a endpoints de cocina            |
| mantenimiento      | Acceso a endpoints de mantenimiento     |

Cada backend puede implementar su lógica de autorización según el rol recibido.

---

## 4. Ejemplo de extracción del rol en Python

```python
import jwt

# jwt_token = ... (obtenido del header Authorization)
# public_key = ... (clave pública RS256)

payload = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
rol = payload["role"]

if rol == "administrador":
    # Permitir acceso total
    pass
elif rol == "nutricionista":
    # Permitir solo endpoints de nutrición
    pass
# ...
```

---

## 5. Notas

- El rol siempre proviene del usuario autenticado, no se acepta por parámetro externo.
- Si el token es inválido o el rol no es reconocido, rechazar la petición con 401/403.
- Mantener la clave pública sincronizada con el backend principal.

---

Para dudas o cambios en la matriz de roles, coordinar con el equipo del backend principal.
