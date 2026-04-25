# censoapp/utils.py
"""
Utilidades para el sistema de censo
Incluye cache de parametros del sistema y otras funciones auxiliares
"""

from django.core.cache import cache
from .models import SystemParameters
import logging

logger = logging.getLogger(__name__)


def get_system_parameters_cached(timeout=3600):
    """
    Obtiene parametros del sistema con cache.
    Por defecto cachea por 1 hora (3600 segundos).

    Args:
        timeout (int): Tiempo de cache en segundos (default: 3600 = 1 hora)

    Returns:
        dict: Diccionario con {key: value} de parametros del sistema

    Example:
        >>> params = get_system_parameters_cached()
        >>> datos_vivienda = params.get('Datos de Vivienda', 'N')
    """
    cache_key = 'system_parameters'
    params = cache.get(cache_key)

    if params is None:
        try:
            params_qs = SystemParameters.objects.all().values('key', 'value')
            params = {p['key']: p['value'] for p in params_qs}
            cache.set(cache_key, params, timeout)
            logger.info(f"Parametros del sistema cacheados: {len(params)} parametros")
        except Exception as e:
            logger.error(f"Error al obtener parametros del sistema: {e}")
            params = {}
    else:
        logger.debug("Parametros del sistema obtenidos desde cache")

    return params


def invalidate_system_parameters_cache():
    """
    Invalida el cache cuando se actualizan parametros del sistema.

    Esta funcion debe llamarse cuando:
    - Se crea un nuevo parametro
    - Se actualiza un parametro existente
    - Se elimina un parametro

    Returns:
        bool: True si se invalido correctamente

    Example:
        >>> invalidate_system_parameters_cache()
        True
    """
    try:
        cache.delete('system_parameters')
        logger.info("Cache de parametros del sistema invalidado")
        return True
    except Exception as e:
        logger.error(f"Error al invalidar cache de parametros: {e}")
        return False


def get_parameter_value(key, default=None, use_cache=True):
    """
    Obtiene el valor de un parametro especifico del sistema.

    Args:
        key (str): Clave del parametro a buscar
        default: Valor por defecto si no se encuentra el parametro
        use_cache (bool): Si True, usa cache; si False, consulta directamente la BD

    Returns:
        str: Valor del parametro o default si no existe

    Example:
        >>> datos_vivienda = get_parameter_value('Datos de Vivienda', 'N')
        >>> print(datos_vivienda)  # 'S' o 'N'
    """
    if use_cache:
        params = get_system_parameters_cached()
        return params.get(key, default)
    else:
        try:
            param = SystemParameters.objects.get(key=key)
            return param.value
        except SystemParameters.DoesNotExist:
            return default

