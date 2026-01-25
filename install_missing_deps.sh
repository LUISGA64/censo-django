#!/bin/bash
# Script de solución completa para PythonAnywhere
# Instala todas las dependencias faltantes

echo "===== INSTALANDO DEPENDENCIAS FALTANTES ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Instalando django-otp (faltante)..."
pip install django-otp==1.2.2

echo ""
echo "2. Instalando otras dependencias críticas..."
pip install qrcode==7.4.2
pip install pillow

echo ""
echo "3. Verificando instalación..."
python manage.py check

echo ""
echo "===== INSTALACIÓN COMPLETADA ====="
echo ""
echo "SIGUIENTE PASO:"
echo "1. Ve a Web Tab"
echo "2. Click en 'Reload'"
echo "3. Prueba tu sitio"
