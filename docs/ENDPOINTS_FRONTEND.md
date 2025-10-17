# 📱 Endpoints para Frontend - API Pharma

Esta guía describe todos los endpoints disponibles para integrar con tu aplicación frontend.

---

## 🔐 Autenticación

### Login (Obtener tokens JWT)
```
POST /api/token/
```
**Body:**
```json
{
  "username": "tu_usuario",
  "password": "tu_password"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Para qué sirve:** Iniciar sesión y obtener tokens de autenticación. Guarda el `access` token para usarlo en los headers de las siguientes peticiones.

---

### Renovar sesión
```
POST /api/token/refresh/
```
**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Para qué sirve:** Obtener un nuevo `access` token cuando el actual expira (cada 30 minutos) sin necesidad de hacer login nuevamente.

---

## 💊 Productos

### Listar todos los productos
```
GET /api/productos/
```
**Query params opcionales:**
- `?ordering=-id` - Ordenar (por id descendente)
- `?ordering=nombre` - Ordenar alfabéticamente
- `?search=aspirina` - Buscar por texto

**Response:**
```json
[
  {
    "id": 1,
    "gtin": "7798140250159",
    "nombre": "Aspirina 500mg x 20",
    "laboratorio": "Bayer",
    "estado": "activo",
    "lotes": [
      {
        "id": 5,
        "numero_lote": "A12345",
        "fecha_venc": "2025-12-31",
        "stock": 50,
        "producto": 1
      }
    ]
  }
]
```
**Para qué sirve:** Mostrar el inventario completo en tu pantalla principal. Incluye los lotes de cada producto.

---

### Crear nuevo producto
```
POST /api/productos/
```
**Body:**
```json
{
  "gtin": "7798140250159",
  "nombre": "Aspirina 500mg x 20",
  "laboratorio": "Bayer",
  "estado": "activo"
}
```
**Para qué sirve:** Agregar un nuevo producto al catálogo manualmente.

---

### Ver detalle de un producto
```
GET /api/productos/{id}/
```
**Ejemplo:** `GET /api/productos/1/`

**Para qué sirve:** Ver toda la información de un producto específico con sus lotes.

---

### Editar producto
```
PUT /api/productos/{id}/     (actualización completa)
PATCH /api/productos/{id}/   (actualización parcial)
```
**Body (PATCH):**
```json
{
  "nombre": "Aspirina 500mg x 30",
  "estado": "inactivo"
}
```
**Para qué sirve:** Modificar nombre, laboratorio o desactivar un producto.

---

### Eliminar producto
```
DELETE /api/productos/{id}/
```
**Para qué sirve:** Borrar un producto del sistema (⚠️ también borra sus lotes).

---

### Vender producto (FEFO automático)
```
POST /api/productos/{id}/egreso-fefo/
```
**Body:**
```json
{
  "cantidad": 5,
  "motivo": "Venta",
  "documento_ref": "FACTURA-001"
}
```
**Response:**
```json
{
  "ok": true,
  "producto": {
    "id": 1,
    "gtin": "7798140250159",
    "nombre": "Aspirina 500mg x 20"
  },
  "lote_usado": {
    "id": 5,
    "numero_lote": "A12345",
    "fecha_venc": "2025-12-31",
    "stock_actual": 45
  }
}
```
**Para qué sirve:** Vender/sacar stock automáticamente del lote que vence primero (FEFO: First-Expire, First-Out). Ideal para el flujo de venta.

---

### Escanear código de barras (Ingreso rápido)
```
POST /api/productos/ingreso-scan/
```
**Body:**
```json
{
  "gtin": "7798140250159",
  "lote": "A12345",
  "fecha_venc": "2025-12-31",
  "cantidad": 1,
  "motivo": "Ingreso por compra",
  "documento_ref": "REMITO-123"
}
```
**Response:**
```json
{
  "ok": true,
  "producto": {
    "id": 1,
    "gtin": "7798140250159",
    "nombre": "Aspirina 500mg x 20",
    "laboratorio": "Bayer",
    "estado": "activo",
    "lotes": [...]
  },
  "lote": {
    "id": 5,
    "numero_lote": "A12345",
    "fecha_venc": "2025-12-31",
    "stock": 51,
    "producto": 1
  }
}
```
**Para qué sirve:** Escanear un código de barras y automáticamente:
- Crea el producto si no existe
- Crea el lote si no existe
- Suma stock (default: 1 unidad)

Perfecto para apps móviles con scanner de códigos de barras.

---

### Buscar producto por código
```
GET /api/scan/{codigo}/
```
**Ejemplo:** `GET /api/scan/7798140250159/`

**Para qué sirve:** Buscar un producto escaneando su GTIN. Retorna 404 si no existe.

---

## 📦 Lotes

### Listar todos los lotes
```
GET /api/lotes/
```
**Query params opcionales:**
- `?ordering=fecha_venc` - Ordenar por vencimiento
- `?ordering=-stock` - Ordenar por stock (descendente)

**Response:**
```json
[
  {
    "id": 5,
    "numero_lote": "A12345",
    "fecha_venc": "2025-12-31",
    "stock": 50,
    "producto": 1
  }
]
```
**Para qué sirve:** Ver todos los lotes del inventario. Útil para pantalla de "Gestión de Lotes".

---

### Crear nuevo lote
```
POST /api/lotes/
```
**Body:**
```json
{
  "producto": 1,
  "numero_lote": "B98765",
  "fecha_venc": "2026-06-30",
  "stock": 0
}
```
**Para qué sirve:** Agregar un nuevo lote manualmente a un producto existente.

---

### Ver detalle de un lote
```
GET /api/lotes/{id}/
```
**Para qué sirve:** Ver información específica de un lote.

---

### Editar lote
```
PUT /api/lotes/{id}/     (actualización completa)
PATCH /api/lotes/{id}/   (actualización parcial)
```
**Body (PATCH):**
```json
{
  "fecha_venc": "2026-12-31"
}
```
**Para qué sirve:** Corregir datos del lote (número, fecha de vencimiento).

⚠️ **Nota:** NO edites el stock directamente. Usa los endpoints de ingreso/egreso/ajuste.

---

### Eliminar lote
```
DELETE /api/lotes/{id}/
```
**Para qué sirve:** Borrar un lote del sistema.

---

### Sumar stock a un lote (Ingreso)
```
POST /api/lotes/{id}/ingreso/
```
**Body:**
```json
{
  "cantidad": 20,
  "motivo": "Compra a proveedor",
  "documento_ref": "REMITO-456"
}
```
**Response:**
```json
{
  "ok": true,
  "lote": {
    "id": 5,
    "numero_lote": "A12345",
    "fecha_venc": "2025-12-31",
    "stock": 70,
    "producto": 1
  }
}
```
**Para qué sirve:** Agregar stock cuando llega mercadería de un proveedor.

---

### Restar stock de un lote (Egreso)
```
POST /api/lotes/{id}/egreso/
```
**Body:**
```json
{
  "cantidad": 10,
  "motivo": "Venta",
  "documento_ref": "FACTURA-789"
}
```
**Para qué sirve:** Restar stock de un lote específico (si querés elegir manualmente el lote, en lugar de usar FEFO automático).

⚠️ **Validaciones:**
- No permite dejar stock negativo
- No permite egreso de lotes vencidos

---

### Ajustar stock de un lote
```
POST /api/lotes/{id}/ajuste/
```
**Body:**
```json
{
  "cantidad": -5,
  "motivo": "Inventario físico",
  "documento_ref": "AJUSTE-2024-10"
}
```
**Para qué sirve:** Ajustar stock manualmente (positivo o negativo) por:
- Inventario físico
- Productos rotos/vencidos
- Correcciones

---

## 📊 Movimientos (Historial/Auditoría)

### Listar historial completo
```
GET /api/movimientos/
```
**Query params opcionales:**
- `?tipo=INGRESO` - Filtrar por tipo (INGRESO, EGRESO, AJUSTE)
- `?lote=5` - Filtrar por lote específico
- `?lote__producto=1` - Filtrar por producto
- `?ordering=-aplicado_en` - Ordenar por fecha (más reciente primero)

**Response:**
```json
[
  {
    "id": 123,
    "lote": 5,
    "tipo": "EGRESO",
    "cantidad": 10,
    "motivo": "Venta",
    "documento_ref": "FACTURA-789",
    "creado_en": "2024-10-17T14:30:00Z",
    "aplicado_en": "2024-10-17T14:30:01Z",
    "usuario": 1,
    "stock_antes": 70,
    "stock_despues": 60
  }
]
```
**Para qué sirve:** Ver el historial completo de todos los movimientos de stock. Ideal para:
- Auditorías
- Trazabilidad
- Ver quién hizo qué y cuándo

---

### Ver detalle de un movimiento
```
GET /api/movimientos/{id}/
```
**Para qué sirve:** Ver información completa de un movimiento específico.

⚠️ **Nota:** Los movimientos son SOLO LECTURA. No se pueden editar ni eliminar (auditoría inmutable).

---

## 📈 Reportes

### Productos próximos a vencer
```
GET /api/reportes/por_vencer/
```
**Query params opcionales:**
- `?dias=30` - Productos que vencen en los próximos 30 días (default: 60)

**Response:**
```json
{
  "hoy": "2024-10-17",
  "dias": 30,
  "items": [
    {
      "lote_id": 8,
      "producto_id": 3,
      "gtin": "7791234567890",
      "producto": "Ibuprofeno 400mg",
      "numero_lote": "X789",
      "fecha_venc": "2024-11-15",
      "stock": 25,
      "dias_restantes": 29
    }
  ]
}
```
**Para qué sirve:** Mostrar alertas de productos próximos a vencer para:
- Hacer promociones
- Avisar al farmacéutico
- Evitar pérdidas por vencimiento

---

## 🎯 Flujos típicos para tu Frontend

### 1. Login de usuario
```
1. POST /api/token/ → Guardar access_token en localStorage/sessionStorage
2. Incluir en todas las peticiones: Header "Authorization: Bearer {access_token}"
```

---

### 2. Pantalla principal (Inventario)
```
GET /api/productos/
↓
Mostrar tabla con: Nombre, GTIN, Stock total, Lotes
```

---

### 3. Ingreso de mercadería (con scanner)
```
1. Escanear código de barras → obtener GTIN
2. POST /api/productos/ingreso-scan/ con { gtin, lote, fecha_venc, cantidad }
3. Mostrar confirmación: "Stock actualizado"
```

---

### 4. Venta de producto
```
Opción A (Recomendada - FEFO automático):
1. POST /api/productos/{id}/egreso-fefo/ con { cantidad, motivo }

Opción B (Lote específico):
1. POST /api/lotes/{id}/egreso/ con { cantidad, motivo }
```

---

### 5. Dashboard con alertas
```
1. GET /api/reportes/por_vencer/?dias=30
   ↓
   Mostrar alerta: "⚠️ 5 productos vencen en los próximos 30 días"

2. GET /api/lotes/?ordering=stock
   ↓
   Mostrar: "Stock bajo: Aspirina (5 unidades)"
```

---

### 6. Historial de movimientos
```
GET /api/movimientos/?tipo=EGRESO&ordering=-aplicado_en
↓
Mostrar tabla con: Fecha, Producto, Tipo, Cantidad, Usuario, Motivo
```

---

## 🔒 Seguridad y Headers

Todas las peticiones (excepto `/api/token/`) deben incluir:

```
Authorization: Bearer {tu_access_token}
Content-Type: application/json
```

Ejemplo con Fetch:
```javascript
fetch('https://tu-api.com/api/productos/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGc...',
    'Content-Type': 'application/json'
  }
})
```

---

## ⚠️ Códigos de error comunes

| Código | Significado | Causa común |
|--------|-------------|-------------|
| 400 | Bad Request | Datos inválidos en el body |
| 401 | Unauthorized | Token expirado o inválido |
| 403 | Forbidden | No tienes permisos (no eres staff) |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Stock insuficiente o lote vencido |

---

## 📝 Notas importantes

1. **Paginación**: Actualmente NO implementada. Si tienes muchos productos, considera agregar `?limit=50&offset=0`

2. **CORS**: Si tu frontend está en otro dominio, necesitas configurar CORS en el backend

3. **Tokens JWT**:
   - `access` expira en 30 minutos
   - `refresh` expira en 7 días
   - Implementa auto-refresh del token en tu frontend

4. **Validaciones**:
   - GTIN debe ser EAN-13 válido (13 dígitos con checksum correcto)
   - Stock nunca puede ser negativo
   - No se pueden hacer egresos de lotes vencidos

5. **Auditoría**:
   - Todos los movimientos registran: usuario, fecha, stock antes/después
   - Los movimientos NO se pueden editar ni eliminar

---

## 🚀 Próximos endpoints recomendados

Para mejorar tu API, considera agregar:
- `GET /api/health/` - Health check
- `GET /api/productos/stock-bajo/` - Productos con stock bajo
- `POST /api/usuarios/registro/` - Registro de usuarios
- `GET /api/dashboard/estadisticas/` - Estadísticas generales

---

**Versión:** 3.0  
**Última actualización:** 17 de Octubre de 2024

