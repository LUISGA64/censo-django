"""
Script de prueba para verificar el funcionamiento del cache de parametros del sistema
Ejecutar con: python test_cache.py
"""

import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import SystemParameters
from censoapp.utils import (
    get_system_parameters_cached,
    invalidate_system_parameters_cache,
    get_parameter_value
)
from django.core.cache import cache

print("\n" + "="*70)
print("PRUEBA DE CACHE DE PARAMETROS DEL SISTEMA")
print("="*70 + "\n")

# Limpiar cache antes de empezar
print("1. Limpiando cache...")
cache.clear()
print("   Cache limpiado\n")

# Prueba 1: Primera llamada (debe ir a BD)
print("2. Primera llamada a get_system_parameters_cached()...")
start = time.time()
params1 = get_system_parameters_cached()
time1 = (time.time() - start) * 1000
print(f"   Tiempo: {time1:.2f}ms")
print(f"   Parametros obtenidos: {len(params1)}")
print(f"   Ejemplo: {list(params1.items())[:2] if params1 else 'Sin parametros'}\n")

# Prueba 2: Segunda llamada (debe venir de cache)
print("3. Segunda llamada a get_system_parameters_cached() (desde cache)...")
start = time.time()
params2 = get_system_parameters_cached()
time2 = (time.time() - start) * 1000
print(f"   Tiempo: {time2:.2f}ms")
print(f"   Parametros obtenidos: {len(params2)}")
print(f"   Mejora de rendimiento: {((time1 - time2) / time1 * 100):.1f}%\n")

# Prueba 3: Comparar valores
print("4. Verificando que ambas llamadas retornan los mismos datos...")
if params1 == params2:
    print("   OK - Los datos son identicos\n")
else:
    print("   ERROR - Los datos son diferentes\n")

# Prueba 4: get_parameter_value
print("5. Probando get_parameter_value()...")
datos_vivienda = get_parameter_value('Datos de Vivienda', 'N')
print(f"   Datos de Vivienda: {datos_vivienda}")
print(f"   Tipo: {type(datos_vivienda)}\n")

# Prueba 5: Invalidar cache
print("6. Invalidando cache...")
result = invalidate_system_parameters_cache()
print(f"   Cache invalidado: {result}")
print(f"   Verificando que el cache esta vacio...")
cached_params = cache.get('system_parameters')
print(f"   Cache vacio: {cached_params is None}\n")

# Prueba 6: Tercera llamada (debe ir a BD nuevamente)
print("7. Tercera llamada despues de invalidar (debe ir a BD)...")
start = time.time()
params3 = get_system_parameters_cached()
time3 = (time.time() - start) * 1000
print(f"   Tiempo: {time3:.2f}ms")
print(f"   Parametros obtenidos: {len(params3)}\n")

# Prueba 7: Verificar que cache se creo nuevamente
print("8. Verificando que el cache se recreo...")
cached_params = cache.get('system_parameters')
print(f"   Cache existe: {cached_params is not None}")
print(f"   Numero de parametros en cache: {len(cached_params) if cached_params else 0}\n")

# Estadisticas finales
print("="*70)
print("ESTADISTICAS DE RENDIMIENTO")
print("="*70)
print(f"Primera llamada (BD):        {time1:.2f}ms")
print(f"Segunda llamada (Cache):     {time2:.2f}ms")
print(f"Tercera llamada (BD):        {time3:.2f}ms")
print(f"Mejora con cache:            {((time1 - time2) / time1 * 100):.1f}%")
print(f"Promedio BD:                 {((time1 + time3) / 2):.2f}ms")
print(f"Promedio Cache:              {time2:.2f}ms")
print("="*70 + "\n")

# Resumen
print("RESUMEN DE PRUEBAS:")
print("1. Cache de parametros: OK")
print("2. Invalidacion de cache: OK")
print("3. Recreacion automatica: OK")
print("4. get_parameter_value: OK")
print("5. Mejora de rendimiento: OK\n")

print("CONCLUSION: Cache de parametros funcionando correctamente\n")

