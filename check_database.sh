#!/bin/bash
# Script para verificar y corregir configuración de base de datos en PythonAnywhere

echo "===== VERIFICANDO CONFIGURACIÓN DE BASE DE DATOS ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Verificando settings_pythonanywhere.py..."
if [ -f "censoProject/settings_pythonanywhere.py" ]; then
    echo "✅ Archivo existe"

    # Verificar qué base de datos está configurada
    echo ""
    echo "2. Configuración actual de base de datos:"
    grep -A 10 "DATABASES = {" censoProject/settings_pythonanywhere.py | head -15

    echo ""
    echo "3. Verificando si existe db.censo_Web (SQLite):"
    if [ -f "db.censo_Web" ]; then
        echo "✅ Base de datos SQLite existe: db.censo_Web"
        ls -lh db.censo_Web
    else
        echo "❌ Base de datos SQLite NO encontrada"
    fi
else
    echo "❌ settings_pythonanywhere.py NO existe"
    echo "📝 Usando settings.py por defecto"
fi

echo ""
echo "4. Archivo WSGI actual apunta a:"
grep "DJANGO_SETTINGS_MODULE" /var/www/luisga64_pythonanywhere_com_wsgi.py

echo ""
echo "===== DIAGNÓSTICO COMPLETADO ====="
echo ""
echo "Si ves 'ENGINE': 'django.db.backends.mysql' arriba,"
echo "pero tienes db.censo_Web (SQLite), hay que cambiar"
echo "la configuración para usar SQLite."
echo ""
echo "Ejecuta: bash fix_database_config.sh"
