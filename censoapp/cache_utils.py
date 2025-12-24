"""
Utilidades de cache para optimizar el rendimiento del sistema.
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
import hashlib
import json


def cache_view(timeout=300, key_prefix='view'):
    """
    Decorador para cachear vistas completas.

    Args:
        timeout: Tiempo en segundos que se mantendrá en cache (default: 5 minutos)
        key_prefix: Prefijo para la clave de cache

    Uso:
        @cache_view(timeout=600, key_prefix='dashboard')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Generar clave única basada en user, org y parámetros
            user_id = request.user.id if request.user.is_authenticated else 'anon'

            # Incluir organización si existe
            org_id = 'none'
            if hasattr(request, 'user_organization') and request.user_organization:
                org_id = request.user_organization.id
            elif request.user.is_authenticated and hasattr(request.user, 'userprofile'):
                try:
                    org_id = request.user.userprofile.organization.id if request.user.userprofile.organization else 'none'
                except:
                    pass

            # Incluir parámetros GET en la clave
            params = request.GET.dict()
            params_str = json.dumps(params, sort_keys=True)
            params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]

            # Construir clave de cache
            cache_key = f"{key_prefix}:user_{user_id}:org_{org_id}:params_{params_hash}"

            # Intentar obtener del cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response

            # Si no está en cache, ejecutar la vista
            response = view_func(request, *args, **kwargs)

            # Guardar en cache
            cache.set(cache_key, response, timeout)

            return response
        return wrapper
    return decorator


def cache_query(timeout=300, key_prefix='query'):
    """
    Decorador para cachear resultados de queries.

    Args:
        timeout: Tiempo en segundos que se mantendrá en cache
        key_prefix: Prefijo para la clave de cache

    Uso:
        @cache_query(timeout=600, key_prefix='personas')
        def obtener_personas():
            return Person.objects.all()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave basada en función y argumentos
            args_str = json.dumps([str(arg) for arg in args], sort_keys=True)
            kwargs_str = json.dumps({k: str(v) for k, v in kwargs.items()}, sort_keys=True)
            combined = f"{args_str}:{kwargs_str}"
            args_hash = hashlib.md5(combined.encode()).hexdigest()[:12]

            cache_key = f"{key_prefix}:{func.__name__}:{args_hash}"

            # Intentar obtener del cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Si no está en cache, ejecutar la función
            result = func(*args, **kwargs)

            # Guardar en cache
            cache.set(cache_key, result, timeout)

            return result
        return wrapper
    return decorator


def invalidate_cache(pattern='*'):
    """
    Invalida cache basado en un patrón.

    Args:
        pattern: Patrón de claves a invalidar (ej: 'dashboard:*', 'personas:*')

    Uso:
        invalidate_cache('dashboard:*')  # Invalida todo el cache del dashboard
    """
    try:
        # Verificar si se está usando Redis
        cache_backend = settings.CACHES['default']['BACKEND']

        if 'redis' in cache_backend.lower():
            # Si es Redis, usar la conexión directa
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")

            # Obtener todas las claves que coincidan con el patrón
            keys = conn.keys(f"censo:{pattern}")

            if keys:
                conn.delete(*keys)
                return len(keys)
            return 0
        else:
            # Si es Local Memory Cache o cualquier otro backend
            # Limpiar todo el cache (no soporta patrones)
            cache.clear()
            return 1
    except Exception as e:
        # Si hay cualquier error, intentar limpiar todo el cache
        try:
            cache.clear()
            return 1
        except:
            print(f"Error al invalidar cache: {e}")
            return 0


def get_or_set_cache(key, callback, timeout=300):
    """
    Helper para obtener del cache o establecer si no existe.

    Args:
        key: Clave de cache
        callback: Función que retorna el valor si no está en cache
        timeout: Tiempo de expiración en segundos

    Uso:
        total_personas = get_or_set_cache(
            'total_personas_org_1',
            lambda: Person.objects.filter(org=1).count(),
            timeout=600
        )
    """
    cached_value = cache.get(key)
    if cached_value is not None:
        return cached_value

    value = callback()
    cache.set(key, value, timeout)
    return value


# Claves de cache predefinidas
CACHE_KEYS = {
    'DASHBOARD_STATS': 'dashboard:stats:org_{org_id}',
    'TOTAL_PERSONAS': 'stats:total_personas:org_{org_id}',
    'TOTAL_FICHAS': 'stats:total_fichas:org_{org_id}',
    'DOCUMENTOS_STATS': 'documentos:stats:org_{org_id}',
    'VEREDAS_STATS': 'veredas:stats:org_{org_id}',
    'EDAD_DISTRIBUTION': 'stats:edad_dist:org_{org_id}',
}


def get_cache_key(key_name, **kwargs):
    """
    Obtiene la clave de cache formateada.

    Uso:
        key = get_cache_key('TOTAL_PERSONAS', org_id=1)
    """
    if key_name in CACHE_KEYS:
        return CACHE_KEYS[key_name].format(**kwargs)
    return key_name

