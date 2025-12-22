# 🔴 Instalación de Redis en Windows

Redis es necesario para el sistema de cache del proyecto.

## Opción 1: Redis para Windows (Memurai - Recomendado)

### Instalación
1. Descargar Memurai (Redis compatible para Windows):
   - https://www.memurai.com/get-memurai
   - Versión gratuita disponible

2. Instalar el archivo descargado
3. Redis se ejecutará automáticamente como servicio de Windows

### Verificar instalación
```powershell
# Verificar que Redis está corriendo
redis-cli ping
# Debería responder: PONG
```

---

## Opción 2: WSL2 (Windows Subsystem for Linux)

### Instalación
```powershell
# 1. Habilitar WSL2
wsl --install

# 2. Reiniciar PC

# 3. En WSL, instalar Redis
sudo apt update
sudo apt install redis-server

# 4. Iniciar Redis
sudo service redis-server start

# 5. Verificar
redis-cli ping
```

---

## Opción 3: Docker (Más Simple)

### Instalación
```powershell
# 1. Instalar Docker Desktop para Windows
# https://www.docker.com/products/docker-desktop

# 2. Ejecutar Redis en container
docker run -d -p 6379:6379 --name redis redis:alpine

# 3. Verificar
docker ps
```

---

## Opción 4: Desarrollo SIN Redis (Fallback)

Si no quieres instalar Redis ahora, el sistema funcionará con cache en memoria:

### Modificar settings.py
```python
# Cambiar configuración de CACHES a:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'censo-cache',
    }
}

# Y comentar SESSION_ENGINE
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
```

**Nota:** El cache en memoria es temporal y se pierde al reiniciar el servidor.

---

## Configuración del Proyecto (Ya está hecha)

El archivo `settings.py` ya tiene la configuración de Redis:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # Fallback a BD si Redis falla
        },
    }
}
```

---

## Verificar que funciona

```python
# En Python shell
python manage.py shell

>>> from django.core.cache import cache
>>> cache.set('test', 'Hola Redis!', 300)
>>> cache.get('test')
# Debería retornar: 'Hola Redis!'
```

---

## Para Producción (Digital Ocean)

En el servidor de producción, instalar Redis es simple:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Redis se instalará automáticamente con el script de despliegue.

---

## Comandos Útiles

```powershell
# Ver todos los keys en Redis
redis-cli KEYS "*"

# Ver valor de un key
redis-cli GET "censo:dashboard:stats:org_1"

# Limpiar todo el cache
redis-cli FLUSHDB

# Ver estadísticas
redis-cli INFO stats
```

---

## Recomendación

**Para desarrollo local:**
- Usar Opción 4 (sin Redis) por simplicidad
- O usar Opción 3 (Docker) si ya tienes Docker

**Para producción:**
- Siempre usar Redis nativo (se instala con el script de despliegue)

---

**El sistema funcionará con o sin Redis**, solo será más rápido con Redis activado.

