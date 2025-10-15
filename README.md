# README

## Problemas y soluciones durante el desarrollo

### 1. Configuración de la base de datos MySQL
- Se configuró el proyecto para usar PyMySQL como driver y se ajustó el archivo `settings.py`.
- Se corrigieron problemas de conexión y se instalaron los paquetes necesarios (`pymysql`, `djangorestframework`, `django-filter`, etc.).

### 2. Migraciones y estructura de la base de datos
- Se presentaron errores de integridad y duplicidad de columnas al aplicar migraciones sobre una base de datos ya existente.
- Se resolvieron eliminando manualmente columnas duplicadas y usando `--fake` en migraciones para sincronizar el estado de Django con la base de datos real.
- Se identificó la necesidad de limpiar o convertir datos en campos de tipo fecha/hora para evitar errores de conversión (`AttributeError: 'str' object has no attribute 'utcoffset'`).
- Se eliminaron y recrearon tablas manualmente cuando fue necesario, y se aplicaron migraciones desde cero.

### 3. Problemas con ALLOWED_HOSTS
- Se corrigió el error `DisallowedHost` agregando `127.0.0.1` a la lista de `ALLOWED_HOSTS` en `settings.py`.

### 4. Creación y gestión de superusuario
- Se creó el superusuario con `--noinput` y luego se asignó la contraseña usando `changepassword`.

### 5. Errores en el admin por tipos de datos
- Se detectaron errores al acceder al admin por valores incorrectos en campos de fecha/hora.
- Se solucionó corrigiendo los datos en la base o eliminando las tablas y recreándolas con migraciones limpias.

### 6. Sincronización de migraciones
- Se usaron los comandos `migrate stock zero --fake` y `migrate stock` para forzar la recreación de tablas cuando Django creía que ya estaban aplicadas.

## Modificaciones realizadas en la base de datos

- Se eliminaron manualmente columnas duplicadas (como `aplicado_en`, `stock_antes`, `stock_despues`, `usuario`) en la tabla `stock_movimientostock` para resolver conflictos de migraciones.
- Se eliminaron y recrearon las tablas `stock_producto`, `stock_lote` y `stock_movimientostock` para limpiar datos incompatibles y asegurar la estructura correcta.
- Se corrigieron valores de tipo string en campos de fecha/hora (`aplicado_en`, `creado_en`, `actualizado_en`) convirtiéndolos a `DATETIME` o asignando `NULL` para evitar errores de conversión en Django.
- Se aplicaron constraints y claves foráneas según los modelos definidos en Django.
- Se usaron comandos SQL como `ALTER TABLE ... DROP COLUMN ...`, `UPDATE ... SET ...`, y `CREATE TABLE ...` para ajustar la estructura y los datos.
- Se sincronizó el estado de las migraciones con la base de datos usando `--fake` y `--fake-initial` cuando fue necesario.

---

Este archivo documenta los principales problemas y soluciones encontradas durante la configuración y puesta en marcha del backend con Django y MySQL.