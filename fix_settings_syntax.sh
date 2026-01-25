#!/bin/bash
# Script para sobrescribir settings_pythonanywhere.py con versión limpia

echo "===== SOBRESCRIBIENDO SETTINGS_PYTHONANYWHERE.PY ====="
echo ""

cd ~/censo-django

echo "1. Eliminando archivo corrupto..."
rm -f censoProject/settings_pythonanywhere.py

echo ""
echo "2. Forzando descarga desde GitHub..."
git checkout origin/development -- censoProject/settings_pythonanywhere.py

echo ""
echo "3. Verificando sintaxis Python..."
python3 -m py_compile censoProject/settings_pythonanywhere.py

if [ $? -eq 0 ]; then
    echo "✅ Archivo válido - Sin errores de sintaxis"
else
    echo "❌ Error en el archivo - Revisar manualmente"
    exit 1
fi

echo ""
echo "4. Instalando dependencias..."
source /home/luisga64/.virtualenvs/censo-env/bin/activate
pip install django-otp==1.2.2 qrcode==7.4.2 pillow

echo ""
echo "5. Creando directorios..."
mkdir -p media/temp_maps media/documents
chmod -R 755 media

echo ""
echo "6. Verificando Django..."
python manage.py check

echo ""
echo "===== COMPLETADO ====="
echo ""
echo "✅ settings_pythonanywhere.py sobrescrito correctamente"
echo "✅ Sin errores de sintaxis"
echo ""
echo "AHORA:"
echo "1. Web Tab -> Reload"
echo "2. Probar sitio"
