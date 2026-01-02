# Guía de Configuración de Settings.py

## ¿Por qué settings.py NO está versionado en Git?

El archivo `settings.py` contiene información sensible y específica de cada entorno:
- **SECRET_KEY**: Clave de seguridad de Django (debe ser diferente en cada entorno)
- **DEBUG**: True en desarrollo, False en producción
- **ALLOWED_HOSTS**: Lista de hosts permitidos (diferente en cada entorno)
- **DATABASES**: Credenciales de base de datos (diferentes en desarrollo y producción)
- **SITE_URL**: URL del sitio (localhost en desarrollo, dominio real en producción)

Por esta razón, `settings.py` está incluido en `.gitignore` para evitar:
1. Exponer credenciales sensibles en el repositorio
2. Conflictos al hacer pull/push entre diferentes entornos
3. Sobrescribir configuraciones de producción accidentalmente

## ¿Afecta esto el despliegue en producción?

**NO**, siempre y cuando sigas estas buenas prácticas:

### 1. Usar settings.example.py como plantilla
El archivo `settings.example.py` **SÍ está versionado** y sirve como plantilla con:
- Estructura completa del archivo de configuración
- Comentarios explicativos
- Valores de ejemplo para desarrollo y producción

### 2. Configuración para diferentes entornos

#### **Desarrollo Local:**
```bash
# Copiar el ejemplo
cp censoProject/settings.example.py censoProject/settings.py

# Editar settings.py con tus valores locales
# - DEBUG = True
# - ALLOWED_HOSTS = []
# - DATABASES: SQLite o MySQL local
# - SECRET_KEY: cualquier valor (no importa en desarrollo)
```

#### **Producción (PythonAnywhere u otro servidor):**
```bash
# En el servidor de producción
cp censoProject/settings.example.py censoProject/settings.py

# Editar settings.py con valores de producción:
# - SECRET_KEY: generar nueva clave única
# - DEBUG = False
# - ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
# - DATABASES: credenciales MySQL de producción
# - SITE_URL = 'https://tu-dominio.com'
```

### 3. Generar SECRET_KEY única para producción
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 4. Usar variables de entorno (Recomendado)
Para mayor seguridad, usa variables de entorno para datos sensibles:

```python
# En settings.py
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-dev-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'censodb'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

## Proceso de Despliegue en Producción

### Primera vez:
1. Hacer pull del código en producción
2. Copiar `settings.example.py` a `settings.py`
3. Editar `settings.py` con configuraciones de producción
4. Ejecutar migraciones: `python manage.py migrate`
5. Recolectar archivos estáticos: `python manage.py collectstatic`
6. Reiniciar el servidor web

### Actualizaciones posteriores:
1. Hacer pull del código actualizado
2. **NO se sobrescribe settings.py** (está en .gitignore)
3. Revisar `settings.example.py` por si hay nuevas configuraciones
4. Si hay cambios en la estructura, actualizar manualmente `settings.py`
5. Ejecutar migraciones si hay cambios en modelos
6. Recolectar archivos estáticos si hay cambios en CSS/JS
7. Reiniciar el servidor web

## Checklist de Seguridad para Producción

- [ ] SECRET_KEY única y diferente a desarrollo
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] DATABASES con credenciales seguras
- [ ] SITE_URL con dominio real (https)
- [ ] Habilitar configuraciones de seguridad:
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  SECURE_BROWSER_XSS_FILTER = True
  SECURE_CONTENT_TYPE_NOSNIFF = True
  ```

## Solución de Problemas

### Error: "No module named 'censoProject.settings'"
- Asegúrate de que existe `censoProject/settings.py`
- Copia desde `settings.example.py` si no existe

### Cambios en settings.example.py no se reflejan
- Es normal, debes actualizar manualmente tu `settings.py` local
- Compara ambos archivos y copia las nuevas configuraciones necesarias

### Conflictos al hacer pull
- No debería haber conflictos porque `settings.py` está en .gitignore
- Si aparecen, es porque no se agregó correctamente al .gitignore

## Alternativa: Múltiples archivos de configuración

Puedes crear diferentes archivos de settings:
```
censoProject/
  settings/
    __init__.py
    base.py          # Configuración común (versionado)
    development.py   # Configuración desarrollo (versionado)
    production.py    # Plantilla producción (versionado)
    local.py         # Configuración personal (NO versionado)
```

Usar según entorno:
```bash
# Desarrollo
export DJANGO_SETTINGS_MODULE=censoProject.settings.development

# Producción
export DJANGO_SETTINGS_MODULE=censoProject.settings.production
```

## Resumen

✅ **SÍ versionar:** `settings.example.py`, documentación
❌ **NO versionar:** `settings.py` (específico de cada entorno)
📝 **Documentar:** Cualquier cambio importante en `settings.example.py`
🔒 **Proteger:** Credenciales, SECRET_KEY, contraseñas

Esta estrategia permite:
- Mantener configuraciones diferentes por entorno
- No exponer información sensible
- Facilitar despliegues sin conflictos
- Documentar la estructura de configuración para otros desarrolladores

