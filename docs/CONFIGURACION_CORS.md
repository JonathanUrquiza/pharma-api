# ✅ Configuración CORS Completada

## 🔧 Cambios realizados

### 1. **Dependencia agregada**
```txt
django-cors-headers
```
Agregado a `requirements.txt` e instalado correctamente.

---

### 2. **Configuración en `settings.py`**

#### App instalada:
```python
INSTALLED_APPS = [
    ...
    "corsheaders",  # ← NUEVO
    ...
]
```

#### Middleware configurado:
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # ← NUEVO (ANTES de CommonMiddleware)
    "django.contrib.sessions.middleware.SessionMiddleware",
    ...
]
```

#### Configuración CORS:
```python
# Permite requests desde CUALQUIER dominio
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Headers permitidos
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Métodos HTTP permitidos
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
```

---

## ✅ ¿Qué permite ahora?

Tu API puede ser consumida desde:
- ✅ `http://localhost:3000` (React, Vue, etc.)
- ✅ `http://localhost:5173` (Vite)
- ✅ `https://tu-frontend.vercel.app`
- ✅ `https://cualquier-dominio.com`
- ✅ Aplicaciones móviles
- ✅ Extensiones de navegador
- ✅ **Cualquier origen**

---

## 🧪 Cómo probar

### Opción 1: Desde el navegador (Console)
Abre la consola del navegador en **cualquier página** y ejecuta:

```javascript
fetch('http://localhost:8000/api/productos/', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(res => res.json())
  .then(data => console.log('✅ CORS funcionando:', data))
  .catch(err => console.error('❌ Error:', err));
```

Si ves los productos en la consola, **CORS está funcionando**.

---

### Opción 2: HTML simple
Crea un archivo `test-cors.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test CORS</title>
</head>
<body>
    <h1>Test API Pharma</h1>
    <button onclick="testAPI()">🧪 Probar GET /productos/</button>
    <button onclick="testLogin()">🔐 Probar Login</button>
    <pre id="resultado"></pre>

    <script>
        const API_URL = 'http://localhost:8000';
        
        async function testAPI() {
            try {
                const response = await fetch(`${API_URL}/api/productos/`);
                const data = await response.json();
                document.getElementById('resultado').textContent = 
                    `✅ CORS OK!\n\n${JSON.stringify(data, null, 2)}`;
            } catch (error) {
                document.getElementById('resultado').textContent = 
                    `❌ Error: ${error.message}`;
            }
        }

        async function testLogin() {
            try {
                const response = await fetch(`${API_URL}/api/token/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: 'admin',
                        password: 'tu_password'
                    })
                });
                const data = await response.json();
                document.getElementById('resultado').textContent = 
                    `✅ Login OK!\n\n${JSON.stringify(data, null, 2)}`;
            } catch (error) {
                document.getElementById('resultado').textContent = 
                    `❌ Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

Abre este archivo en tu navegador y haz clic en los botones.

---

### Opción 3: Desde React/Vue/Angular

**React (fetch):**
```javascript
useEffect(() => {
  fetch('http://localhost:8000/api/productos/')
    .then(res => res.json())
    .then(data => setProductos(data))
    .catch(err => console.error(err));
}, []);
```

**React (axios):**
```javascript
import axios from 'axios';

axios.get('http://localhost:8000/api/productos/')
  .then(res => setProductos(res.data))
  .catch(err => console.error(err));
```

**Vue 3:**
```javascript
const productos = ref([]);

onMounted(async () => {
  const response = await fetch('http://localhost:8000/api/productos/');
  productos.value = await response.json();
});
```

---

## ⚠️ Advertencia de seguridad

**Configuración actual:**
```python
CORS_ALLOW_ALL_ORIGINS = True  # ← Permite CUALQUIER dominio
```

Esto está bien para **desarrollo**, pero en **producción** es recomendable restringir los dominios:

```python
# En producción, cambia a:
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend-produccion.com",
    "https://www.tu-frontend-produccion.com",
    "https://app.tu-dominio.com",
]
```

---

## 🔄 Ejemplo completo con autenticación

```javascript
// 1. Login
const loginResponse = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'tu_password'
  })
});
const { access } = await loginResponse.json();

// 2. Usar el token en requests
const productosResponse = await fetch('http://localhost:8000/api/productos/', {
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json'
  }
});
const productos = await productosResponse.json();

// 3. Crear un producto
const nuevoProducto = await fetch('http://localhost:8000/api/productos/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    gtin: '7798140250159',
    nombre: 'Aspirina 500mg',
    laboratorio: 'Bayer',
    estado: 'activo'
  })
});
```

---

## 📋 Checklist de verificación

- [x] `django-cors-headers` instalado
- [x] `corsheaders` agregado a `INSTALLED_APPS`
- [x] `CorsMiddleware` agregado a `MIDDLEWARE` (ANTES de `CommonMiddleware`)
- [x] `CORS_ALLOW_ALL_ORIGINS = True` configurado
- [x] Headers y métodos permitidos configurados

---

## 🚀 Próximos pasos recomendados

1. **Prueba desde tu frontend** (React, Vue, etc.)
2. **En producción:** Cambia `CORS_ALLOW_ALL_ORIGINS` a `False` y usa `CORS_ALLOWED_ORIGINS` con tu dominio real
3. **Considera agregar:** Rate limiting con `django-ratelimit` o DRF throttling
4. **HTTPS:** En producción, asegúrate de usar HTTPS tanto en backend como frontend

---

## 🆘 Troubleshooting

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"
**Causa:** El middleware no está correctamente configurado.
**Solución:** Verifica que `CorsMiddleware` esté ANTES de `CommonMiddleware` en `MIDDLEWARE`.

### Error: "CORS policy: Request header field authorization is not allowed"
**Causa:** El header `Authorization` no está en `CORS_ALLOW_HEADERS`.
**Solución:** Ya está agregado en la configuración actual.

### Error: "CORS policy: Method PUT/DELETE is not allowed"
**Causa:** El método no está en `CORS_ALLOW_METHODS`.
**Solución:** Ya está agregado en la configuración actual.

### El servidor no inicia después de los cambios
**Solución:** Reinicia el servidor Django:
```bash
python manage.py runserver
```

---

**Estado:** ✅ CORS configurado y funcionando  
**Fecha:** 17 de Octubre de 2024  
**Configuración:** Permite todos los orígenes (development mode)

