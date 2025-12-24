"""
Script para optimizar espacio del proyecto AUTOMÁTICAMENTE.
Elimina archivos innecesarios para el despliegue.
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_size_mb(path):
    """Calcula el tamaño en MB"""
    if os.path.isfile(path):
        return os.path.getsize(path) / (1024 * 1024)
    
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)


def limpiar_proyecto_auto():
    """Elimina archivos innecesarios automáticamente"""
    
    print("=" * 70)
    print("🧹 OPTIMIZACIÓN AUTOMÁTICA DEL PROYECTO")
    print("=" * 70)
    print()
    
    eliminados = 0
    espacio_liberado = 0
    
    # 1. Carpetas completas a eliminar
    carpetas_eliminar = [
        'venv',      # Entorno virtual (no va a producción)
        'frontend',  # No se usa en producción
        '.idea',     # Config PyCharm
    ]
    
    print("🗂️  ELIMINANDO CARPETAS PESADAS...")
    for carpeta in carpetas_eliminar:
        path = BASE_DIR / carpeta
        if path.exists():
            size = get_size_mb(path)
            try:
                shutil.rmtree(path)
                print(f"   ✅ {carpeta:20s} : {size:>10.2f} MB")
                eliminados += 1
                espacio_liberado += size
            except Exception as e:
                print(f"   ❌ Error en {carpeta}: {e}")
    
    print()
    
    # 2. Archivos grandes innecesarios
    archivos_grandes = [
        'db.censo_Web',  # Base de datos local
        'debug.log',     # Logs de desarrollo
    ]
    
    print("📄 ELIMINANDO ARCHIVOS GRANDES...")
    for archivo in archivos_grandes:
        path = BASE_DIR / archivo
        if path.exists():
            size = get_size_mb(path)
            try:
                path.unlink()
                print(f"   ✅ {archivo:30s} : {size:>10.2f} MB")
                eliminados += 1
                espacio_liberado += size
            except Exception as e:
                print(f"   ❌ Error en {archivo}: {e}")
    
    print()
    
    # 3. Documentación antigua (mantener solo archivos de despliegue)
    docs_mantener = [
        'DEPLOY_PYTHONANYWHERE_RAPIDO.md',
        'GUIA_DESPLIEGUE_PYTHONANYWHERE.md',
        'CHECKLIST_DESPLIEGUE_PYTHONANYWHERE.md',
        'RESUMEN_DESPLIEGUE_PYTHONANYWHERE.md',
        'PRUEBA_CARGA_MASIVA_FINAL.md',
        'GUIA_BUSQUEDA_GLOBAL.md',
        'GUIA_IMPORTACION_MASIVA.md',
        'README.md',
    ]
    
    print("📝 ELIMINANDO DOCUMENTACIÓN ANTIGUA...")
    eliminados_docs = 0
    for item in BASE_DIR.glob('*.md'):
        if item.name not in docs_mantener:
            size = get_size_mb(item)
            try:
                item.unlink()
                eliminados_docs += 1
                espacio_liberado += size
            except Exception as e:
                pass
    
    for item in BASE_DIR.glob('*.txt'):
        if item.name not in ['requirements.txt']:
            try:
                size = get_size_mb(item)
                item.unlink()
                eliminados_docs += 1
                espacio_liberado += size
            except Exception as e:
                pass
    
    print(f"   ✅ {eliminados_docs} archivos de documentación eliminados")
    print()
    
    # 4. Scripts temporales
    print("🔧 ELIMINANDO SCRIPTS TEMPORALES...")
    scripts_mantener = [
        'manage.py',
        'crear_datos_demo.py',
        'limpiar_datos_auto.py',
        'limpiar_datos_prueba.py',
    ]
    
    eliminados_scripts = 0
    for item in BASE_DIR.glob('*.py'):
        if item.name not in scripts_mantener and item.name != Path(__file__).name:
            try:
                size = get_size_mb(item)
                item.unlink()
                eliminados_scripts += 1
                espacio_liberado += size
            except Exception as e:
                pass
    
    print(f"   ✅ {eliminados_scripts} scripts temporales eliminados")
    print()
    
    # 5. Scripts de shell innecesarios
    print("📜 ELIMINANDO SCRIPTS SHELL...")
    scripts_shell = BASE_DIR.glob('*.sh')
    eliminados_shell = 0
    for script in scripts_shell:
        try:
            size = get_size_mb(script)
            script.unlink()
            eliminados_shell += 1
            espacio_liberado += size
        except Exception as e:
            pass
    
    print(f"   ✅ {eliminados_shell} scripts shell eliminados")
    print()
    
    # 6. Archivos PowerShell innecesarios
    ps_files = [
        'recreate_db.ps1',
        'comandos_rapidos.ps1',
    ]
    
    for ps_file in ps_files:
        path = BASE_DIR / ps_file
        if path.exists():
            try:
                size = get_size_mb(path)
                path.unlink()
                espacio_liberado += size
            except Exception as e:
                pass
    
    # 7. Limpiar __pycache__ y archivos .pyc
    print("🧽 LIMPIANDO CACHE DE PYTHON...")
    cache_eliminado = 0
    for root, dirs, files in os.walk(BASE_DIR):
        # Eliminar carpetas __pycache__
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_path)
                cache_eliminado += 1
            except:
                pass
        
        # Eliminar archivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    print(f"   ✅ {cache_eliminado} carpetas cache eliminadas")
    print()
    
    # Resumen final
    print("=" * 70)
    print("✅ OPTIMIZACIÓN COMPLETADA")
    print("=" * 70)
    print(f"   💾 Espacio liberado: {espacio_liberado:.2f} MB")
    print()
    print("📁 ARCHIVOS MANTENIDOS PARA DESPLIEGUE:")
    print("-" * 70)
    print("   ✅ Código fuente (censoapp, censoProject, templates)")
    print("   ✅ Archivos estáticos (static/)")
    print("   ✅ Requirements.txt")
    print("   ✅ Guías de despliegue PythonAnywhere")
    print("   ✅ Scripts de utilidad (crear_datos_demo, limpiar_datos)")
    print("   ✅ Configuraciones (.env.example, settings)")
    print()
    print("🚀 PROYECTO OPTIMIZADO Y LISTO PARA DESPLIEGUE")
    print("=" * 70)


if __name__ == '__main__':
    limpiar_proyecto_auto()

