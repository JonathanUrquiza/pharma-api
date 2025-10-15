#  – Endpoints (v)

- **Base URLs**: —
- **Autenticación global**: —

## Matriz de Endpoints
| Método | Ruta | operationId | Descripción | Auth | Consumes | Produces |
|---|---|---|---|---|---|---|
| GET | `/api/lotes/` | listLotes | — | — | — | application/json |
| POST | `/api/lotes/` | createLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| GET | `/api/lotes/{id}/` | retrieveLote | — | — | — | application/json |
| PUT | `/api/lotes/{id}/` | updateLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | application/json |
| PATCH | `/api/lotes/{id}/` | partialUpdateLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | application/json |
| DELETE | `/api/lotes/{id}/` | destroyLote | — | — | — | — |
| POST | `/api/lotes/{id}/ajuste/` | ajusteLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| POST | `/api/lotes/{id}/egreso/` | egresoLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| POST | `/api/lotes/{id}/ingreso/` | ingresoLote | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| GET | `/api/movimientos/` | listMovimientoStocks | — | — | — | application/json |
| GET | `/api/movimientos/{id}/` | retrieveMovimientoStock | — | — | — | application/json |
| GET | `/api/productos/` | listProductos | — | — | — | application/json |
| POST | `/api/productos/` | createProducto | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| POST | `/api/productos/ingreso-scan/` | ingresoScanProducto | Crea o busca Producto + Lote a partir de un scan y suma 1 (o 'cantidad') al stock. | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| GET | `/api/productos/{id}/` | retrieveProducto | — | — | — | application/json |
| PUT | `/api/productos/{id}/` | updateProducto | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | application/json |
| PATCH | `/api/productos/{id}/` | partialUpdateProducto | — | — | application/json, application/x-www-form-urlencoded, multipart/form-data | application/json |
| DELETE | `/api/productos/{id}/` | destroyProducto | — | — | — | — |
| POST | `/api/productos/{id}/egreso-fefo/` | egresoFefoProducto | POST /api/productos/{id}/egreso-fefo | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| GET | `/api/reportes/por_vencer/` | listlotes_por_vencers | /api/reportes/por_vencer/?dias=60 Devuelve lotes con stock>0 que vencen en <= N días (default 60). | — | — | application/json |
| GET | `/api/scan/{codigo}/` | retrievescan | — | — | — | application/json |
| POST | `/api/token/` | createTokenObtainPair | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |
| POST | `/api/token/refresh/` | createTokenRefresh | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. | — | application/json, application/x-www-form-urlencoded, multipart/form-data | — |

## Detalle por Endpoint

### `/api/lotes/`

#### GET
- **operationId**: `listLotes`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 200: — (content: application/json)

#### POST
- **operationId**: `createLote`
- **Resumen**: —
_Sin parámetros_
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 201: — (content: application/json)

### `/api/lotes/{id}/`

#### GET
- **operationId**: `retrieveLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 200: — (content: application/json)

#### PUT
- **operationId**: `updateLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 200: — (content: application/json)

#### PATCH
- **operationId**: `partialUpdateLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 200: — (content: application/json)

#### DELETE
- **operationId**: `destroyLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 204: — (content: —)

### `/api/lotes/{id}/ajuste/`

#### POST
- **operationId**: `ajusteLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 201: — (content: application/json)

### `/api/lotes/{id}/egreso/`

#### POST
- **operationId**: `egresoLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 201: — (content: application/json)

### `/api/lotes/{id}/ingreso/`

#### POST
- **operationId**: `ingresoLote`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este lote. |
**Request Body**:
- application/json: `Lote`
- application/x-www-form-urlencoded: `Lote`
- multipart/form-data: `Lote`
**Responses**:
- 201: — (content: application/json)

### `/api/movimientos/`

#### GET
- **operationId**: `listMovimientoStocks`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| query | tipo | string | False |  |
| query | lote | string | False |  |
| query | lote__producto | string | False |  |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
**Responses**:
- 200: — (content: application/json)

### `/api/movimientos/{id}/`

#### GET
- **operationId**: `retrieveMovimientoStock`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este movimiento stock. |
| query | tipo | string | False |  |
| query | lote | string | False |  |
| query | lote__producto | string | False |  |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
**Responses**:
- 200: — (content: application/json)

### `/api/productos/`

#### GET
- **operationId**: `listProductos`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 200: — (content: application/json)

#### POST
- **operationId**: `createProducto`
- **Resumen**: —
_Sin parámetros_
**Request Body**:
- application/json: `Producto`
- application/x-www-form-urlencoded: `Producto`
- multipart/form-data: `Producto`
**Responses**:
- 201: — (content: application/json)

### `/api/productos/ingreso-scan/`

#### POST
- **operationId**: `ingresoScanProducto`
- **Resumen**: Crea o busca Producto + Lote a partir de un scan y suma 1 (o 'cantidad') al stock.
_Sin parámetros_
**Request Body**:
- application/json: `Producto`
- application/x-www-form-urlencoded: `Producto`
- multipart/form-data: `Producto`
**Responses**:
- 201: — (content: application/json)

### `/api/productos/{id}/`

#### GET
- **operationId**: `retrieveProducto`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este producto. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 200: — (content: application/json)

#### PUT
- **operationId**: `updateProducto`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este producto. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Request Body**:
- application/json: `Producto`
- application/x-www-form-urlencoded: `Producto`
- multipart/form-data: `Producto`
**Responses**:
- 200: — (content: application/json)

#### PATCH
- **operationId**: `partialUpdateProducto`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este producto. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Request Body**:
- application/json: `Producto`
- application/x-www-form-urlencoded: `Producto`
- multipart/form-data: `Producto`
**Responses**:
- 200: — (content: application/json)

#### DELETE
- **operationId**: `destroyProducto`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este producto. |
| query | ordering | string | False | Qué campo usar para ordenar los resultados. |
| query | search | string | False | Un término de búsqueda. |
**Responses**:
- 204: — (content: —)

### `/api/productos/{id}/egreso-fefo/`

#### POST
- **operationId**: `egresoFefoProducto`
- **Resumen**: POST /api/productos/{id}/egreso-fefo
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | id | string | True | Un valor de entero único que identifique este producto. |
**Request Body**:
- application/json: `Producto`
- application/x-www-form-urlencoded: `Producto`
- multipart/form-data: `Producto`
**Responses**:
- 201: — (content: application/json)

### `/api/reportes/por_vencer/`

#### GET
- **operationId**: `listlotes_por_vencers`
- **Resumen**: /api/reportes/por_vencer/?dias=60 Devuelve lotes con stock>0 que vencen en <= N días (default 60).
_Sin parámetros_
**Responses**:
- 200: — (content: application/json)

### `/api/scan/{codigo}/`

#### GET
- **operationId**: `retrievescan`
- **Resumen**: —
**Parámetros**:
| En | Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|---|
| path | codigo | string | True |  |
**Responses**:
- 200: — (content: application/json)

### `/api/token/`

#### POST
- **operationId**: `createTokenObtainPair`
- **Resumen**: Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
_Sin parámetros_
**Request Body**:
- application/json: `TokenObtainPair`
- application/x-www-form-urlencoded: `TokenObtainPair`
- multipart/form-data: `TokenObtainPair`
**Responses**:
- 201: — (content: application/json)

### `/api/token/refresh/`

#### POST
- **operationId**: `createTokenRefresh`
- **Resumen**: Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.
_Sin parámetros_
**Request Body**:
- application/json: `TokenRefresh`
- application/x-www-form-urlencoded: `TokenRefresh`
- multipart/form-data: `TokenRefresh`
**Responses**:
- 201: — (content: application/json)

## Reglas de Negocio (Farmacia)
- Validación EAN-13 y GS1 DataMatrix (rechazo si checksum inválido).
- Prohibición de stock negativo (HTTP 409 al intentar dejar stock < 0).
- FEFO (First-Expire, First-Out) para ventas/salidas.
- Bloqueo automático de productos vencidos.
- Trazabilidad: todos los movimientos generan registro de auditoría (usuario, timestamp, antes/después, motivo).
