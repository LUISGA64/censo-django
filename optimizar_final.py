"""
Script FINAL de optimización para PythonAnywhere.
Elimina imágenes decorativas innecesarias y optimiza al máximo.
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_size_mb(path):
    """Calcula tamaño en MB"""
    if os.path.isfile(path):
        return os.path.getsize(path) / (1024 * 1024)

    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)


def optimizar_final():
    """Optimización final del proyecto"""

    print("=" * 70)
    print("🚀 OPTIMIZACIÓN FINAL PARA PYTHONANYWHERE")
    print("=" * 70)
    print()

    espacio_liberado = 0

    # 1. Eliminar imágenes decorativas grandes del tema
    print("🖼️  ELIMINANDO IMÁGENES DECORATIVAS...")

    carpeta_imagenes = BASE_DIR / 'static' / 'assets' / 'img'

    # Imágenes decorativas que no se usan en el proyecto
    imagenes_decorativas = [
        'curved-images',  # Todas las imágenes curved
        'home-decor-1.jpg',
        'home-decor-2.jpg',
        'home-decor-3.jpg',
    ]

    for item in imagenes_decorativas:
        path = carpeta_imagenes / item
        if path.exists():
            size = get_size_mb(path)
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"   ✅ {item:30s} : {size:>10.2f} MB")
                espacio_liberado += size
            except Exception as e:
                print(f"   ❌ Error: {e}")

    print()

    # 2. Eliminar archivos de documentación de vendors
    print("📄 ELIMINANDO DOCS DE LIBRERÍAS...")

    vendors_path = BASE_DIR / 'static' / 'vendors'
    docs_eliminados = 0

    if vendors_path.exists():
        for vendor_dir in vendors_path.iterdir():
            if vendor_dir.is_dir():
                # Eliminar carpetas docs, examples, tests
                for subfolder in ['docs', 'examples', 'tests', 'test']:
                    docs_folder = vendor_dir / subfolder
                    if docs_folder.exists():
                        size = get_size_mb(docs_folder)
                        try:
                            shutil.rmtree(docs_folder)
                            docs_eliminados += 1
                            espacio_liberado += size
                        except:
                            pass

    print(f"   ✅ {docs_eliminados} carpetas de documentación eliminadas")
    print()

    # 3. Eliminar archivos .map (sourcemaps)
    print("🗺️  ELIMINANDO SOURCEMAPS...")

    map_files = list(BASE_DIR.rglob('*.map'))
    map_size = sum(get_size_mb(f) for f in map_files)

    for map_file in map_files:
        try:
            map_file.unlink()
        except:
            pass

    print(f"   ✅ {len(map_files)} archivos .map eliminados ({map_size:.2f} MB)")
    espacio_liberado += map_size
    print()

    # 4. Eliminar archivos no minificados cuando existe versión .min
    print("📦 ELIMINANDO VERSIONES NO MINIFICADAS...")

    eliminados_no_min = 0
    size_no_min = 0

    # Buscar archivos .js y .css que tengan versión .min
    for ext in ['*.js', '*.css']:
        for archivo in BASE_DIR.rglob(ext):
            if '.min.' not in archivo.name and not archivo.name.endswith('.min.js') and not archivo.name.endswith('.min.css'):
                # Verificar si existe versión minificada
                min_version = archivo.parent / (archivo.stem + '.min' + archivo.suffix)
                if min_version.exists():
                    size = get_size_mb(archivo)
                    try:
                        archivo.unlink()
                        eliminados_no_min += 1
                        size_no_min += size
                    except:
                        pass

    print(f"   ✅ {eliminados_no_min} archivos no minificados eliminados ({size_no_min:.2f} MB)")
    espacio_liberado += size_no_min
    print()

    # 5. Limpiar media/temp
    print("🧹 LIMPIANDO ARCHIVOS TEMPORALES...")

    temp_path = BASE_DIR / 'media' / 'temp'
    if temp_path.exists():
        size = get_size_mb(temp_path)
        try:
            shutil.rmtree(temp_path)
            temp_path.mkdir(exist_ok=True)
            print(f"   ✅ media/temp limpiado ({size:.2f} MB)")
            espacio_liberado += size
        except:
            pass

    # Crear archivo .gitkeep
    gitkeep = temp_path / '.gitkeep'
    gitkeep.touch(exist_ok=True)

    print()

    # Resumen final
    print("=" * 70)
    print("✅ OPTIMIZACIÓN FINAL COMPLETADA")
    print("=" * 70)
    print(f"   💾 Espacio total liberado: {espacio_liberado:.2f} MB")
    print()

    # Mostrar tamaño final por carpeta
    print("📊 TAMAÑO FINAL POR CARPETA:")
    print("-" * 70)

    carpetas = ['static', 'censoapp', 'censoProject', 'templates', 'media', 'docs', 'scripts']

    total_proyecto = 0
    for carpeta in carpetas:
        path = BASE_DIR / carpeta
        if path.exists():
            size = get_size_mb(path)
            total_proyecto += size
            print(f"   {carpeta:20s} : {size:>10.2f} MB")

    print("-" * 70)
    print(f"   {'TOTAL PROYECTO':20s} : {total_proyecto:>10.2f} MB")
    print()

    print("✅ ARCHIVOS MANTENIDOS:")
    print("   • Código fuente completo")
    print("   • Templates del sistema")
    print("   • Static files necesarios (minificados)")
    print("   • Guías de despliegue PythonAnywhere")
    print("   • Scripts de utilidad")
    print("   • Requirements.txt")
    print()
    print("❌ ARCHIVOS ELIMINADOS:")
    print("   • Imágenes decorativas del tema")
    print("   • Documentación de librerías")
    print("   • Sourcemaps (.map)")
    print("   • Versiones no minificadas")
    print("   • Archivos temporales")
    print()
    print("🚀 PROYECTO OPTIMIZADO PARA PYTHONANYWHERE")
    print(f"   Tamaño total: ~{total_proyecto:.0f} MB (sin venv)")
    print()
    print("💡 NOTA: La carpeta 'venv' NO debe subirse a GitHub ni PythonAnywhere")
    print("         Se recreará con: pip install -r requirements.txt")
    print("=" * 70)


if __name__ == '__main__':
    optimizar_final()

