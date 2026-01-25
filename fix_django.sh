#!/bin/bash
# Script de solución para error Django Session en PythonAnywhere
# Ejecutar con: bash fix_django.sh

echo "===== INICIANDO SOLUCIÓN DE DJANGO SESSION ERROR ====="
echo ""

# Ir al directorio del proyecto
cd ~/censo-django

# Activar entorno virtual
echo "1. Activando entorno virtual..."
source venv/bin/activate

# Ver versión actual
echo ""
echo "2. Versión actual de Django:"
pip show django | grep Version

# Desinstalar Django problemático
echo ""
echo "3. Desinstalando Django problemático..."
pip uninstall django -y

# Instalar Django 5.0.0 estable
echo ""
echo "4. Instalando Django 5.0.0 (estable)..."
pip install Django==5.0.0

# Reinstalar dependencias
echo ""
echo "5. Reinstalando dependencias compatibles..."
pip install django-allauth==0.57.0
pip install django-mfa2==2.6.0

# Limpiar sesiones
echo ""
echo "6. Limpiando sesiones corruptas..."
python manage.py clearsessions

# Migrar base de datos
echo ""
echo "7. Migrando base de datos..."
python manage.py migrate --run-syncdb

# Verificar
echo ""
echo "8. Verificando instalación..."
python manage.py check

# Instalar folium
echo ""
echo "9. Instalando folium para mapas..."
pip install folium==0.15.1

# Resumen final
echo ""
echo "===== RESUMEN FINAL ====="
echo "Django instalado:"
pip show django | grep Version
echo ""
echo "Folium instalado:"
pip list | grep folium
echo ""
echo "===== SOLUCIÓN COMPLETADA ====="
echo ""
echo "SIGUIENTE PASO:"
echo "1. Ve a Web Tab en PythonAnywhere"
echo "2. Click en el botón 'Reload' (verde grande)"
echo "3. Prueba tu sitio: https://luisga64.pythonanywhere.com/"
echo ""
