#!/bin/bash
# Script de solución completa para PythonAnywhere
# Instala dependencias y configura permisos

echo "===== SOLUCIONANDO TODOS LOS PROBLEMAS ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Creando directorios necesarios..."
mkdir -p media/temp_maps
mkdir -p media/documents
mkdir -p tmp
mkdir -p staticfiles

echo ""
echo "2. Configurando permisos..."
chmod -R 755 media
chmod -R 755 tmp
chmod -R 755 staticfiles

echo ""
echo "3. Instalando django-otp (faltante)..."
pip install django-otp==1.2.2

echo ""
echo "4. Instalando otras dependencias críticas..."
pip install qrcode==7.4.2
pip install pillow

echo ""
echo "5. Verificando instalación..."
python manage.py check

echo ""
echo "===== SOLUCIÓN COMPLETADA ====="
echo ""
echo "Directorios creados y con permisos:"
ls -la media/
echo ""
echo "SIGUIENTE PASO:"
echo "1. Ve a Web Tab"
echo "2. Click en 'Reload'"
echo "3. Prueba tu sitio: https://luisga64.pythonanywhere.com/"
echo ""
echo "✅ Todo listo para funcionar"
