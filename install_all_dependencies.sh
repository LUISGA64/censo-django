#!/bin/bash
# Script para instalar TODAS las dependencias necesarias en PythonAnywhere

echo "===== INSTALANDO TODAS LAS DEPENDENCIAS ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Instalando Django y extensiones principales..."
pip install Django==5.0.0
pip install django-allauth==0.57.0
pip install django-mfa2==2.6.0
pip install django-otp==1.2.2

echo ""
echo "2. Instalando utilidades de autenticación..."
pip install qrcode==7.4.2
pip install pillow

echo ""
echo "3. Instalando REST Framework y filtros..."
pip install djangorestframework
pip install django-filter
pip install coreapi

echo ""
echo "4. Instalando formularios y estilos..."
pip install django-crispy-forms
pip install crispy-bootstrap5

echo ""
echo "5. Instalando utilidades generales..."
pip install python-decouple
pip install django-cors-headers
pip install django-simple-history

echo ""
echo "6. Instalando folium para mapas..."
pip install folium==0.15.1

echo ""
echo "7. Actualizando código desde GitHub..."
git pull origin development

echo ""
echo "8. Creando directorios..."
mkdir -p media/temp_maps media/documents tmp
chmod -R 755 media tmp

echo ""
echo "9. Verificando instalación..."
echo "Paquetes Django instalados:"
pip list | grep -i django
echo ""
echo "Verificando Django..."
python manage.py check

echo ""
echo "===== INSTALACIÓN COMPLETADA ====="
echo ""
echo "Dependencias instaladas:"
echo "✅ Django 5.0.0"
echo "✅ django-allauth"
echo "✅ django-mfa2"
echo "✅ django-otp"
echo "✅ qrcode + pillow"
echo "✅ djangorestframework"
echo "✅ django-filter"
echo "✅ crispy-forms"
echo "✅ folium"
echo "✅ Y todas las demás dependencias"
echo ""
echo "SIGUIENTE PASO:"
echo "1. Ve a Web Tab"
echo "2. Click en 'Reload'"
echo "3. Prueba tu sitio: https://luisga64.pythonanywhere.com/"
echo ""
echo "✅ Todo listo para funcionar"
