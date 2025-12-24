"""
Script para analizar y optimizar el espacio del proyecto.
Identifica y elimina archivos innecesarios para el despliegue.
"""
import os
import shutil
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent


def get_size_mb(path):
    """Calcula el tamaño de un archivo o directorio en MB"""
    if os.path.isfile(path):
        return os.path.getsize(path) / (1024 * 1024)
    
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)


def analizar_proyecto():
    """Analiza el tamaño de carpetas y archivos del proyecto"""
    print("=" * 70)
    print("ANÁLISIS DE ESPACIO DEL PROYECTO")
    print("=" * 70)
    print()
    
    # Analizar carpetas principales
    carpetas = [
        'media', 'static', 'frontend', 'docs', 'templates', 
        'censoapp', 'censoProject', 'scripts', 'venv'
    ]
    
    print("📊 TAMAÑO POR CARPETA:")
    print("-" * 70)
    
    tamaños = []
    for carpeta in carpetas:
        path = BASE_DIR / carpeta
        if path.exists():
            size = get_size_mb(path)
            tamaños.append((carpeta, size))
            print(f"   {carpeta:20s} : {size:>10.2f} MB")
    
    print("-" * 70)
    print(f"   {'TOTAL':20s} : {sum(s for _, s in tamaños):>10.2f} MB")
    print()
    
    # Archivos grandes en raíz
    print("📄 ARCHIVOS GRANDES EN RAÍZ:")
    print("-" * 70)
    
    archivos_raiz = []
    for item in BASE_DIR.iterdir():
        if item.is_file():
            size = get_size_mb(item)
            if size > 0.1:  # Más de 100KB
                archivos_raiz.append((item.name, size))
    
    archivos_raiz.sort(key=lambda x: x[1], reverse=True)
    
    for nombre, size in archivos_raiz[:10]:
        print(f"   {nombre:40s} : {size:>10.2f} MB")
    
    print()
    
    return tamaños, archivos_raiz


def identificar_archivos_innecesarios():
    """Identifica archivos y carpetas que pueden eliminarse"""
    print("=" * 70)
    print("ARCHIVOS INNECESARIOS IDENTIFICADOS")
    print("=" * 70)
    print()
    
    innecesarios = {
        'carpetas': [],
        'archivos': []
    }
    
    # Carpetas completas que pueden eliminarse
    carpetas_eliminar = [
        'frontend',  # No se usa en producción
        'venv',      # No debe subirse a producción
        '.idea',     # Configuración PyCharm
    ]
    
    for carpeta in carpetas_eliminar:
        path = BASE_DIR / carpeta
        if path.exists():
            size = get_size_mb(path)
            innecesarios['carpetas'].append((carpeta, path, size))
    
    # Archivos específicos que pueden eliminarse
    archivos_eliminar = [
        'db.censo_Web',  # Base de datos local (no necesaria)
        'debug.log',     # Logs locales
        'migrate_data.py',  # Script temporal
        'verificacion_final_sistema.py',  # Script temporal
        '*.pyc',  # Archivos compilados Python
        '__pycache__',  # Cache de Python
    ]
    
    # Archivos de documentación antiguos (mantener solo los de despliegue)
    docs_antiguos = [
        'BUSQUEDA_GLOBAL_QUICK.md',
        'CHECKLIST_DESPLIEGUE.md',
        'COMANDOS_SERVIDOR.md',
        'CONSOLIDACION_DOCUMENTACION.md',
        'CONTINUAR_DESDE_CASA.md',
        'CORRECCION_FIELDERROR_BUSQUEDA.md',
        'CORRECCION_LOGIN.md',
        'DESPLIEGUE_RAPIDO.md',
        'EJECUTAR_MIGRACION.md',
        'GUIA_DESPLIEGUE_DIGITAL_OCEAN.md',
        'IMPORTACION_DATOS_VIVIENDA_OPCIONALES.md',
        'INICIO_RAPIDO_VARIABLES.txt',
        'INSTALACION_REDIS.md',
        'INSTRUCCIONES_RECREAR_BD.md',
        'MEJORAS_IMPLEMENTADAS_V1.1.md',
        'PROBLEMAS_RESUELTOS.md',
        'README_DATOS_PRUEBA.md',
        'README_SEGUIMIENTO.md',
        'RESUMEN_DESPLIEGUE.md',
        'RESUMEN_FINAL_COMPLETO.md',
        'RESUMEN_FINAL_VARIABLES.md',
        'ROADMAP_SIGUIENTE_FASE.md',
        'SOLUCION_PANTALLA_BLANCO_IMPORTACION.md',
    ]
    
    for doc in docs_antiguos:
        path = BASE_DIR / doc
        if path.exists():
            size = get_size_mb(path)
            innecesarios['archivos'].append((doc, path, size))
    
    # Scripts temporales
    for item in BASE_DIR.glob('*.py'):
        if item.name not in ['manage.py', 'crear_datos_demo.py', 'limpiar_datos_auto.py', 'limpiar_datos_prueba.py']:
            if 'eliminar' in item.name or 'verificar' in item.name or 'migrate' in item.name:
                size = get_size_mb(item)
                innecesarios['archivos'].append((item.name, item, size))
    
    # Mostrar resumen
    print("🗂️  CARPETAS A ELIMINAR:")
    print("-" * 70)
    total_carpetas = 0
    for nombre, path, size in innecesarios['carpetas']:
        print(f"   {nombre:30s} : {size:>10.2f} MB")
        total_carpetas += size
    print(f"   {'Subtotal':30s} : {total_carpetas:>10.2f} MB")
    print()
    
    print("📄 ARCHIVOS A ELIMINAR:")
    print("-" * 70)
    total_archivos = 0
    for nombre, path, size in innecesarios['archivos']:
        print(f"   {nombre:40s} : {size:>10.2f} MB")
        total_archivos += size
    print(f"   {'Subtotal':40s} : {total_archivos:>10.2f} MB")
    print()
    
    print("=" * 70)
    print(f"💾 ESPACIO TOTAL A LIBERAR: {total_carpetas + total_archivos:.2f} MB")
    print("=" * 70)
    print()
    
    return innecesarios


def limpiar_proyecto(innecesarios, confirmar=True):
    """Elimina los archivos innecesarios identificados"""
    
    if confirmar:
        print()
        respuesta = input("⚠️  ¿Deseas eliminar estos archivos? (si/no): ")
        if respuesta.lower() not in ['si', 'sí', 's', 'yes', 'y']:
            print("❌ Operación cancelada.")
            return
    
    print()
    print("🗑️  ELIMINANDO ARCHIVOS...")
    print()
    
    eliminados = 0
    espacio_liberado = 0
    
    # Eliminar carpetas
    for nombre, path, size in innecesarios['carpetas']:
        try:
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"   ✅ Carpeta eliminada: {nombre} ({size:.2f} MB)")
                    eliminados += 1
                    espacio_liberado += size
        except Exception as e:
            print(f"   ❌ Error al eliminar {nombre}: {e}")
    
    # Eliminar archivos
    for nombre, path, size in innecesarios['archivos']:
        try:
            if path.exists():
                path.unlink()
                print(f"   ✅ Archivo eliminado: {nombre} ({size:.2f} MB)")
                eliminados += 1
                espacio_liberado += size
        except Exception as e:
            print(f"   ❌ Error al eliminar {nombre}: {e}")
    
    print()
    print("=" * 70)
    print(f"✅ LIMPIEZA COMPLETADA")
    print(f"   Elementos eliminados: {eliminados}")
    print(f"   Espacio liberado: {espacio_liberado:.2f} MB")
    print("=" * 70)


def main():
    print()
    print("🧹 OPTIMIZACIÓN DE ESPACIO DEL PROYECTO")
    print()
    
    # Analizar proyecto
    analizar_proyecto()
    
    # Identificar archivos innecesarios
    innecesarios = identificar_archivos_innecesarios()
    
    # Limpiar proyecto
    limpiar_proyecto(innecesarios, confirmar=True)
    
    print()
    print("📊 ANÁLISIS POST-LIMPIEZA:")
    print()
    analizar_proyecto()


if __name__ == '__main__':
    main()

